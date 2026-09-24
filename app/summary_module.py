"""
Summary Module - Summarizes long paragraphs into concise versions
"""
import logging
import re
from typing import Dict
from .config import has_gemini_key, get_gemini_model_name

logger = logging.getLogger(__name__)

def _fallback_summarize(text: str) -> str:
    """Fallback summarization using extractive approach"""
    text = text.strip()
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= 2:
        return text  # Already short
    
    # Simple extractive summarization: first sentence + most keyword-rich + last
    # Count word frequency
    words = re.findall(r'\b\w+\b', text.lower())
    common = {'the', 'is', 'are', 'was', 'were', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that', 'these', 'those', 'it', 'its', 'as', 'be', 'been', 'have', 'has', 'had', 'will', 'would', 'can', 'could', 'should', 'may', 'might', 'do', 'does', 'did'}
    filtered_words = [w for w in words if w not in common and len(w) > 3]
    
    from collections import Counter
    word_freq = Counter(filtered_words)
    
    # Score sentences by keyword frequency
    scored = []
    for idx, sent in enumerate(sentences):
        sent_words = re.findall(r'\b\w+\b', sent.lower())
        score = sum(word_freq.get(w, 0) for w in sent_words)
        # Boost first and last sentences slightly
        if idx == 0:
            score += 5
        if idx == len(sentences) - 1:
            score += 3
        scored.append((score, idx, sent))
    
    # Sort by score, take top 30% or at least 2 sentences, max 4
    num_to_take = max(2, min(4, len(sentences) // 3 + 1))
    scored.sort(reverse=True)
    selected = sorted(scored[:num_to_take], key=lambda x: x[1])  # Sort back by original order
    
    summary_sentences = [s[2] for s in selected]
    summary = ' '.join(summary_sentences)
    
    # Add fallback header
    result = f"""**Summary (Fallback Mode - {len(text)} → {len(summary)} chars, {len(sentences)} → {len(summary_sentences)} sentences):**

{summary}

---
*Key points retained: {', '.join([w for w,_ in word_freq.most_common(5)]) if word_freq else 'main concepts'}*

*Note: This is extractive summarization fallback. Configure GEMINI_API_KEY for AI-powered abstractive summarization that retains core information while eliminating redundancy.*
"""
    return result

def summarize_text(text: str) -> Dict:
    """
    Summarize long paragraph into concise version
    """
    if not text or not text.strip():
        return {"error": "Text cannot be empty", "summary": None}
    
    text = text.strip()
    
    if len(text) < 50:
        return {"error": "Text too short to summarize (min 50 chars)", "summary": None}
    
    # If text is already short (< 200 chars), return as is with note
    if len(text) < 200:
        return {
            "summary": text,
            "source": "no-op",
            "model": "none",
            "original_length": len(text),
            "summary_length": len(text),
            "note": "Text already concise, no summarization needed"
        }
    
    # Try Gemini
    if has_gemini_key():
        try:
            import google.generativeai as genai
            from .config import GEMINI_API_KEY
            
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(get_gemini_model_name())
            
            prompt = f"""You are EduGenie, an AI summarization assistant for students.

Task: Summarize the following educational passage into a concise, easy-to-understand version.

Requirements:
- Retain core information and key points
- Eliminate redundancy
- Keep it clear and student-friendly
- Use bullet points if helpful
- Length: 30-40% of original
- Ensure clarity and context preserved
- Ideal for quick revision

Original text ({len(text)} chars):
\"\"\"{text}\"\"\"

Provide concise summary:"""
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                summary = response.text.strip()
                return {
                    "summary": summary,
                    "source": "gemini",
                    "model": get_gemini_model_name(),
                    "original_length": len(text),
                    "summary_length": len(summary),
                    "compression_ratio": f"{len(summary)/len(text)*100:.1f}%"
                }
            else:
                logger.warning("Gemini empty response for summary")
                fallback = _fallback_summarize(text)
                return {
                    "summary": fallback,
                    "source": "fallback",
                    "model": "fallback",
                    "original_length": len(text),
                    "summary_length": len(fallback),
                    "note": "Gemini empty response"
                }
                
        except Exception as e:
            logger.error(f"Gemini summary error: {e}")
            fallback = _fallback_summarize(text)
            return {
                "summary": fallback,
                "source": "fallback",
                "model": "fallback",
                "original_length": len(text),
                "summary_length": len(fallback),
                "error_detail": str(e)
            }
    else:
        fallback = _fallback_summarize(text)
        return {
            "summary": fallback,
            "source": "fallback",
            "model": "fallback",
            "original_length": len(text),
            "summary_length": len(fallback),
            "note": "No API key, using fallback"
        }
