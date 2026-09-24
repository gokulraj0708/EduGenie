"""
EduGenie - FastAPI Main Application
Google Gemini Powered Learning Assistant
"""
import os
import logging
from pathlib import Path
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

# Import modules
from .qna import answer_question
from .explanation_module import explain_concept
from .quiz_module import generate_quiz
from .summary_module import summarize_text
from .learning_path import get_learning_recommendations
from .config import has_gemini_key, get_gemini_model_name

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    description="Google Gemini Powered Learning Assistant that simplifies learning through generative AI",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Setup paths
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Ensure directories exist
TEMPLATES_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# Templates and static
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Pydantic models for API
class QARequest(BaseModel):
    query: Optional[str] = None
    # Support both 'query' and 'question' field for compatibility
    question: Optional[str] = None
    
    def get_query(self):
        return self.query or self.question or ""

class ExplainRequest(BaseModel):
    topic: Optional[str] = None
    # Support alternative field names
    text: Optional[str] = None
    concept: Optional[str] = None
    
    def get_topic(self):
        return self.topic or self.text or self.concept or ""

class QuizRequest(BaseModel):
    text: Optional[str] = None
    topic: Optional[str] = None
    passage: Optional[str] = None
    
    def get_text(self):
        return self.text or self.topic or self.passage or ""

class SummaryRequest(BaseModel):
    text: Optional[str] = None
    passage: Optional[str] = None
    content: Optional[str] = None
    
    def get_text(self):
        return self.text or self.passage or self.content or ""

class LearningPathRequest(BaseModel):
    topic: Optional[str] = None
    text: Optional[str] = None
    
    def get_topic(self):
        return self.topic or self.text or ""

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve main frontend"""
    return templates.TemplateResponse(request, "index.html", {
        "has_api_key": has_gemini_key(),
        "model_name": get_gemini_model_name()
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "EduGenie",
        "version": "1.0.0",
        "gemini_configured": has_gemini_key(),
        "model": get_gemini_model_name() if has_gemini_key() else "fallback",
        "endpoints": ["/qa", "/explain", "/quiz", "/summarize", "/learn/recommendations"]
    }

@app.get("/api/status")
async def api_status():
    """API status with more details"""
    return {
        "status": "operational",
        "service": "EduGenie - Google Gemini Powered Learning Assistant",
        "features": {
            "qna": "Ask questions and receive smart answers",
            "explain": "Understand complex concepts through simplified explanations",
            "quiz": "Generate quizzes from topics or text",
            "summarize": "Summarize large educational passages",
            "learning_path": "Receive personalized learning recommendations"
        },
        "gemini_configured": has_gemini_key(),
        "model": get_gemini_model_name(),
        "fallback_available": True
    }

# Core API Endpoints as per reference doc
@app.post("/qa")
async def qa_endpoint(request: QARequest):
    """
    QnA Module - Ask questions and receive smart, concise answers
    """
    try:
        query = request.get_query().strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        result = answer_question(query)
        
        if "error" in result and result.get("answer") is None:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"QA endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/explain")
async def explain_endpoint(request: ExplainRequest):
    """
    Explanation Module - Understand complex concepts through simplified explanations
    Uses LaMini-Flan-T5 logic with Gemini fallback
    """
    try:
        topic = request.get_topic().strip()
        if not topic:
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        result = explain_concept(topic)
        
        if "error" in result and result.get("explanation") is None:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Explain endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/quiz")
async def quiz_endpoint(request: QuizRequest):
    """
    Quiz Module - Generate three MCQs from a given passage
    Each with 4 options, JSON format
    """
    try:
        text = request.get_text().strip()
        if not text:
            raise HTTPException(status_code=400, detail="Text/topic cannot be empty")
        
        result = generate_quiz(text)
        
        if "error" in result and result.get("quiz") is None:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Quiz endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/summarize")
async def summarize_endpoint(request: SummaryRequest):
    """
    Summary Module - Summarize long paragraphs into concise versions
    """
    try:
        text = request.get_text().strip()
        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        result = summarize_text(text)
        
        if "error" in result and result.get("summary") is None:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Summarize endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/learn/recommendations")
async def learning_path_endpoint(request: LearningPathRequest):
    """
    Learning Path Module - Receive personalized learning recommendations
    Structured plan with beginner to advanced topics, timelines, suggestions
    """
    try:
        topic = request.get_topic().strip()
        if not topic:
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        result = get_learning_recommendations(topic)
        
        if "error" in result and result.get("learning_path") is None:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Learning path endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Additional compatibility endpoints
@app.post("/api/qa")
async def api_qa_compat(request: QARequest):
    return await qa_endpoint(request)

@app.post("/api/explain")
async def api_explain_compat(request: ExplainRequest):
    return await explain_endpoint(request)

@app.post("/api/quiz")
async def api_quiz_compat(request: QuizRequest):
    return await quiz_endpoint(request)

@app.post("/api/summarize")
async def api_summarize_compat(request: SummaryRequest):
    return await summarize_endpoint(request)

@app.post("/api/learn/recommendations")
async def api_learning_compat(request: LearningPathRequest):
    return await learning_path_endpoint(request)

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api/") or request.url.path in ["/qa", "/explain", "/quiz", "/summarize", "/learn/recommendations"]:
        return JSONResponse(status_code=404, content={"detail": "Endpoint not found", "path": request.url.path})
    return templates.TemplateResponse(request, "index.html", {"has_api_key": has_gemini_key(), "model_name": get_gemini_model_name()}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    from .config import HOST, PORT
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
