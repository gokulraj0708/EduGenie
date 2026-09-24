"""
Quiz Module - Generates 3 MCQs with 4 options each from given text/topic
"""
import logging
import json
import re
import random
from typing import Dict, List
from .config import has_gemini_key, get_gemini_model_name

logger = logging.getLogger(__name__)

def clean_json_block(text: str) -> str:
    """Clean markdown code blocks from JSON response - as described in reference doc"""
    if not text:
        return ""
    
    # Remove ```json and ``` markers
    text = re.sub(r'^```json\s*', '', text.strip(), flags=re.MULTILINE)
    text = re.sub(r'^```\s*', '', text.strip(), flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text.strip(), flags=re.MULTILINE)
    
    # Remove any leading/trailing whitespace
    text = text.strip()
    
    return text

def _fallback_quiz_generation(text: str) -> List[Dict]:
    """Generate fallback quiz when Gemini unavailable"""
    text = text.strip()
    topic = text[:50]  # Use first 50 chars as topic hint
    
    # Extract potential keywords for more relevant questions
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter common words
    common = {'the', 'is', 'are', 'was', 'were', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that', 'these', 'those', 'it', 'its'}
    keywords = [w for w in words if w not in common and len(w) > 3]
    unique_keywords = list(dict.fromkeys(keywords))[:10]  # Keep order, unique
    
    if not unique_keywords:
        unique_keywords = ["concept", "principle", "application", "theory"]
    
    # Template questions that work for any topic
    quiz = [
        {
            "question": f"What is the main focus of '{topic}...'?",
            "options": [
                f"Understanding the core principles of {unique_keywords[0] if len(unique_keywords) > 0 else 'the topic'}",
                f"Memorizing unrelated facts about {unique_keywords[1] if len(unique_keywords) > 1 else 'random topics'}",
                f"Ignoring the importance of {unique_keywords[0] if len(unique_keywords) > 0 else 'learning'}",
                f"Avoiding study of {topic[:20]}"
            ],
            "correct_answer": f"Understanding the core principles of {unique_keywords[0] if len(unique_keywords) > 0 else 'the topic'}",
            "explanation": f"The passage primarily discusses {unique_keywords[0] if len(unique_keywords) > 0 else 'the main topic'} and its fundamentals."
        },
        {
            "question": f"Which of the following best describes an important aspect of '{topic[:30]}'?",
            "options": [
                f"It involves {unique_keywords[1] if len(unique_keywords) > 1 else 'key concepts'} and practical applications",
                f"It is completely unrelated to education",
                f"It has no real-world use",
                f"It should be avoided by students"
            ],
            "correct_answer": f"It involves {unique_keywords[1] if len(unique_keywords) > 1 else 'key concepts'} and practical applications",
            "explanation": f"The text emphasizes {unique_keywords[1] if len(unique_keywords) > 1 else 'important concepts'} and their relevance."
        },
        {
            "question": f"What would be the best way to learn more about '{topic[:30]}'?",
            "options": [
                "Practice with examples, ask questions, and explore learning paths",
                "Ignore all study materials",
                "Only memorize without understanding",
                "Avoid asking questions"
            ],
            "correct_answer": "Practice with examples, ask questions, and explore learning paths",
            "explanation": "Active learning through practice and questioning is the most effective approach, as suggested by EduGenie's learning methodology."
        }
    ]
    
    # If we have more keywords, make questions more specific
    if len(text) > 100 and len(unique_keywords) >= 3:
        quiz[0] = {
            "question": f"Based on the text, what is significant about '{unique_keywords[0]}'?",
            "options": [
                f"{unique_keywords[0].capitalize()} is a key concept discussed in the context of {unique_keywords[1] if len(unique_keywords) > 1 else 'the topic'}",
                f"{unique_keywords[0].capitalize()} is irrelevant to the discussion",
                f"{unique_keywords[0].capitalize()} should be ignored",
                f"{unique_keywords[0].capitalize()} has no definition"
            ],
            "correct_answer": f"{unique_keywords[0].capitalize()} is a key concept discussed in the context of {unique_keywords[1] if len(unique_keywords) > 1 else 'the topic'}",
            "explanation": f"The passage mentions {unique_keywords[0]} as an important element."
        }
    
    return quiz

def generate_quiz(text: str) -> Dict:
    """
    Generate 3 MCQs from given passage/topic
    Expected output: JSON format with questions, 4 options each, correct answer
    """
    if not text or not text.strip():
        return {"error": "Input text/topic cannot be empty", "quiz": None}
    
    text = text.strip()
    
    if len(text) < 5:
        return {"error": "Input too short, please provide more context", "quiz": None}
    
    # Try Gemini if available
    if has_gemini_key():
        try:
            import google.generativeai as genai
            from .config import GEMINI_API_KEY
            
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(get_gemini_model_name())
            
            prompt = f"""You are EduGenie, an AI quiz generator for students.

Task: Generate exactly 3 multiple-choice questions (MCQs) from the given text/topic.

Input: "{text}"

Requirements:
- Generate 3 MCQs
- Each question must have 4 options (A, B, C, D)
- Each question must have 1 correct answer
- Make distractors plausible but clearly incorrect
- Questions should test understanding, not just memorization
- Cover different aspects of the input
- Return ONLY valid JSON array, no extra text, no markdown

Expected JSON format:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Brief explanation why this is correct"
  }},
  {{
    "question": "Second question?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option B",
    "explanation": "Explanation"
  }},
  {{
    "question": "Third question?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option C",
    "explanation": "Explanation"
  }}
]

Important:
- correct_answer must exactly match one of the options
- Ensure valid JSON
- No markdown code blocks, just raw JSON
- Keep questions clear and student-friendly

Generate the quiz now:"""
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                cleaned = clean_json_block(response.text)
                try:
                    quiz_data = json.loads(cleaned)
                    
                    # Validate structure
                    if isinstance(quiz_data, list) and len(quiz_data) == 3:
                        # Validate each question
                        valid = True
                        for q in quiz_data:
                            if not all(k in q for k in ["question", "options", "correct_answer"]):
                                valid = False
                                break
                            if len(q["options"]) != 4:
                                valid = False
                                break
                            if q["correct_answer"] not in q["options"]:
                                valid = False
                                break
                        
                        if valid:
                            return {
                                "quiz": quiz_data,
                                "source": "gemini",
                                "model": get_gemini_model_name(),
                                "input_text": text[:200] + "..." if len(text) > 200 else text
                            }
                    
                    # If validation failed, try to use what we have or fallback
                    logger.warning(f"Quiz validation failed, raw: {cleaned[:500]}")
                    # Try fallback if invalid
                    return {
                        "quiz": _fallback_quiz_generation(text),
                        "source": "fallback",
                        "model": "fallback",
                        "input_text": text[:200] + "..." if len(text) > 200 else text,
                        "note": "Gemini response invalid format, used fallback",
                        "raw_response": cleaned[:500]
                    }
                    
                except json.JSONDecodeError as je:
                    logger.error(f"JSON parse error: {je}, raw: {cleaned[:500]}")
                    return {
                        "quiz": _fallback_quiz_generation(text),
                        "source": "fallback",
                        "model": "fallback",
                        "input_text": text,
                        "note": "Failed to parse Gemini JSON, used fallback",
                        "parse_error": str(je)
                    }
            else:
                return {
                    "quiz": _fallback_quiz_generation(text),
                    "source": "fallback",
                    "model": "fallback",
                    "input_text": text,
                    "note": "Gemini empty response"
                }
                
        except Exception as e:
            logger.error(f"Gemini quiz error: {e}")
            return {
                "quiz": _fallback_quiz_generation(text),
                "source": "fallback",
                "model": "fallback",
                "input_text": text,
                "error_detail": str(e),
                "note": "Gemini API failed, used fallback"
            }
    else:
        # No API key
        return {
            "quiz": _fallback_quiz_generation(text),
            "source": "fallback",
            "model": "fallback",
            "input_text": text,
            "note": "No API key configured, using fallback"
        }
