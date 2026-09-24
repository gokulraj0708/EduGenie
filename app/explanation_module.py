"""
Explanation Module - Simplifies complex concepts
Original spec: LaMini-Flan-T5-783M (local) for concept explanation
Implementation: Tries local model if available, else Gemini, else fallback templated explanation
"""
import logging
import re
from typing import Dict
from .config import has_gemini_key, get_gemini_model_name, USE_LOCAL_MODEL

logger = logging.getLogger(__name__)

def _fallback_explanation(topic: str) -> str:
    """Generate structured fallback explanation"""
    topic = topic.strip()
    
    return f"""# {topic} - Simplified Explanation (Fallback Mode)

## 📚 What is {topic}?

**{topic}** is an important concept in education that can be understood through simple breakdown.

### 🔍 Simple Definition:
{topic} refers to a fundamental idea or principle that helps us understand how things work in this domain. Think of it as a building block for more advanced learning.

### 🧩 Key Components:
1. **Core Idea**: The central principle behind {topic}
2. **How it Works**: The mechanism or process involved
3. **Why it Matters**: Its importance and real-world applications
4. **Common Examples**: Everyday instances where you see {topic}

### 💡 Easy Analogy:
Imagine {topic} like learning to ride a bicycle - at first it seems complex with many parts (balance, pedaling, steering), but once you understand each component separately, the whole concept becomes clear and intuitive.

### 📝 Detailed Breakdown:

**Step 1: Foundation**
- Start with the basic definition
- Understand the origin and purpose
- Identify where it's used

**Step 2: Core Mechanics**
- How does {topic} function?
- What are the main rules or principles?
- What makes it unique?

**Step 3: Real-World Application**
- Where do we see {topic} in daily life?
- How do professionals use it?
- What problems does it solve?

**Step 4: Common Misconceptions**
- Beginners often confuse {topic} with similar concepts
- Remember: It's not just theory, but has practical value
- Practice with examples helps solidify understanding

### ✅ Quick Summary:
- **In one sentence**: {topic} is a key concept that helps us understand and solve problems in its field.
- **Remember**: Break complex topics into smaller parts, use analogies, and practice with examples.

### 🎯 Next Steps:
- Try asking EduGenie to generate a quiz on "{topic}"
- Request a learning path for "{topic}" to get structured study plan
- Ask specific questions using QnA feature

*Note: This is a fallback explanation. Configure GEMINI_API_KEY for AI-powered personalized explanations using Gemini 1.5 Pro and LaMini-Flan-T5 logic.*
"""

def _try_local_model(topic: str) -> str:
    """Try to use local LaMini-Flan-T5 model if available and requested"""
    if not USE_LOCAL_MODEL:
        return None
    
    try:
        from transformers import pipeline
        # Try to load LaMini-Flan-T5-783M - this is heavy, may fail
        # Use smaller alternative if not available
        logger.info("Attempting to load local model for explanation...")
        
        # Try lightweight model first
        try:
            pipe = pipeline("text2text-generation", model="MBZUAI/LaMini-Flan-T5-783M", device=-1)
        except:
            # Fallback to even smaller model
            pipe = pipeline("text2text-generation", model="google/flan-t5-small", device=-1)
        
        prompt = f"Explain {topic} in simple terms for a student. Use clear, concise language:"
        result = pipe(prompt, max_length=512, do_sample=False)
        
        if result and len(result) > 0:
            return result[0]['generated_text']
        
    except Exception as e:
        logger.warning(f"Local model failed: {e}")
        return None
    
    return None

def explain_concept(topic: str) -> Dict:
    """
    Explain a concept in simplified manner
    """
    if not topic or not topic.strip():
        return {"error": "Topic cannot be empty", "explanation": None}
    
    topic = topic.strip()
    
    # Try local model first if configured
    local_result = _try_local_model(topic)
    if local_result:
        return {
            "explanation": local_result,
            "source": "local_model",
            "model": "LaMini-Flan-T5-783M",
            "topic": topic
        }
    
    # Try Gemini if available
    if has_gemini_key():
        try:
            import google.generativeai as genai
            from .config import GEMINI_API_KEY
            
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(get_gemini_model_name())
            
            prompt = f"""You are EduGenie, an AI educational assistant specialized in simplifying complex concepts.

Task: Explain "{topic}" in a simple, student-friendly way.

Requirements:
- Use simple, clear language suitable for beginners
- Break down complex ideas into easy parts
- Include analogy or real-world example
- Structure: Definition, Key Points, Analogy, Summary
- Keep it concise but comprehensive (200-300 words)
- Use emojis and formatting for readability
- Make it engaging for students

Topic to explain: {topic}

Provide your simplified explanation:"""
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                return {
                    "explanation": response.text.strip(),
                    "source": "gemini",
                    "model": get_gemini_model_name(),
                    "topic": topic
                }
            else:
                logger.warning("Gemini returned empty for explanation")
                return {
                    "explanation": _fallback_explanation(topic),
                    "source": "fallback",
                    "model": "fallback",
                    "topic": topic,
                    "note": "Gemini empty response"
                }
                
        except Exception as e:
            logger.error(f"Gemini explanation error: {e}")
            return {
                "explanation": _fallback_explanation(topic),
                "source": "fallback",
                "model": "fallback",
                "topic": topic,
                "error_detail": str(e)
            }
    else:
        # Fallback
        return {
            "explanation": _fallback_explanation(topic),
            "source": "fallback",
            "model": "fallback",
            "topic": topic,
            "note": "No API key, using fallback"
        }
