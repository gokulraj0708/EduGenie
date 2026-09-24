"""
QnA Module - Handles general question answering using Gemini
"""
import logging
from typing import Dict
from .config import has_gemini_key, get_gemini_model_name

logger = logging.getLogger(__name__)

# Fallback knowledge base for demo/testing without API key
FALLBACK_KNOWLEDGE = {
    "ocean": "The Pacific Ocean is the largest and deepest ocean on Earth, covering about 30% of the Earth's surface area. It is larger than all landmasses combined.",
    "river": "The Nile River is traditionally considered the longest river in the world at about 6,650 km, while the Amazon is the largest by discharge volume.",
    "pythagoras": "The Pythagoras Theorem states that in a right-angled triangle, the square of the hypotenuse equals the sum of squares of the other two sides: a² + b² = c².",
    "sql": "SQL (Structured Query Language) is used to manage and manipulate relational databases. Key concepts include SELECT, INSERT, UPDATE, DELETE, JOINs, and normalization.",
}

def _get_fallback_answer(query: str) -> str:
    """Generate a helpful fallback answer when Gemini is unavailable"""
    q_lower = query.lower()
    
    # Check for keywords
    for keyword, knowledge in FALLBACK_KNOWLEDGE.items():
        if keyword in q_lower:
            return f"**Answer (Fallback Mode):**\n\n{knowledge}\n\n*Note: This is a fallback response. For more detailed AI-powered answers, configure GEMINI_API_KEY.*\n\n**Additional context for '{query}':**\nThis topic is important in education. To learn more, try asking for a detailed explanation or learning path using EduGenie's other features."
    
    # Generic fallback
    return f"""**Answer (Fallback Mode):**

Your question: "{query}"

This is an excellent educational question! While I would normally use Google Gemini 1.5 Pro for a detailed AI-powered response, I'm currently running in fallback mode (no API key configured).

**Here's a structured approach to understand this topic:**

1. **Definition**: {query} is an important concept that requires understanding its fundamentals.
2. **Key Points**: Break it down into smaller components and understand each part.
3. **Examples**: Look for real-world applications and examples.
4. **Practice**: Try related problems or quizzes to test understanding.

**To get AI-powered detailed answer:**
- Configure your GEMINI_API_KEY in .env file
- Restart the application

*Tip: You can also use EduGenie's Explain feature for simplified explanations, or Learning Path for structured study plan.*

Source: Fallback knowledge system
"""

def answer_question(query: str) -> Dict:
    """
    Answer a question using Gemini API with fallback
    """
    if not query or not query.strip():
        return {"error": "Query cannot be empty", "answer": None}
    
    query = query.strip()
    
    # Try Gemini if API key available
    if has_gemini_key():
        try:
            import google.generativeai as genai
            from .config import GEMINI_API_KEY, get_gemini_model_name
            
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(get_gemini_model_name())
            
            prompt = f"""You are EduGenie, an AI educational assistant. Answer the following student question concisely, accurately, and in a student-friendly manner.

Question: {query}

Provide:
- A clear, concise answer
- Key points if applicable
- Simple language suitable for students
- If relevant, include examples

Answer:"""
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                return {
                    "answer": response.text.strip(),
                    "source": "gemini",
                    "model": get_gemini_model_name(),
                    "query": query
                }
            else:
                logger.warning("Gemini returned empty response, using fallback")
                return {
                    "answer": _get_fallback_answer(query),
                    "source": "fallback",
                    "model": "fallback",
                    "query": query,
                    "note": "Gemini returned empty response"
                }
                
        except Exception as e:
            logger.error(f"Gemini API error: {e}, using fallback")
            return {
                "answer": _get_fallback_answer(query),
                "source": "fallback",
                "model": "fallback",
                "query": query,
                "error_detail": str(e),
                "note": "Gemini API failed, used fallback"
            }
    else:
        # No API key, use fallback
        return {
            "answer": _get_fallback_answer(query),
            "source": "fallback",
            "model": "fallback",
            "query": query,
            "note": "No API key configured, using fallback"
        }
