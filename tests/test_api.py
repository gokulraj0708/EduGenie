"""
Test suite for EduGenie API endpoints
Tests all 5 core modules: QnA, Explain, Quiz, Summarize, Learning Path
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "EduGenie"
    assert "endpoints" in data
    print("✓ Health check passed")

def test_api_status():
    """Test API status endpoint"""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "features" in data
    assert "qna" in data["features"]
    print("✓ API status passed")

def test_home_page():
    """Test home page serves HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text
    assert "Google Gemini Powered Learning Assistant" in response.text
    print("✓ Home page passed")

def test_qa_endpoint():
    """Test QnA module - Ask questions"""
    # Valid query
    response = client.post("/qa", json={"query": "Which is the largest ocean?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 20
    assert "source" in data
    print(f"✓ QnA valid query passed - source: {data['source']}")
    
    # Test with alternative field
    response = client.post("/qa", json={"question": "What is photosynthesis?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    print("✓ QnA alternative field passed")
    
    # Empty query should fail
    response = client.post("/qa", json={"query": ""})
    assert response.status_code == 400
    print("✓ QnA empty validation passed")

def test_explain_endpoint():
    """Test Explanation module"""
    response = client.post("/explain", json={"topic": "The Pythagoras Theorem"})
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert len(data["explanation"]) > 50
    assert "Pythagoras" in data["explanation"] or "pythagoras" in data["explanation"].lower() or "theorem" in data["explanation"].lower()
    print(f"✓ Explain module passed - source: {data['source']}")
    
    # Empty topic
    response = client.post("/explain", json={"topic": ""})
    assert response.status_code == 400
    print("✓ Explain validation passed")

def test_quiz_endpoint():
    """Test Quiz module - Generates 3 MCQs"""
    test_text = "Photosynthesis is the process by which green plants use sunlight to synthesize foods from carbon dioxide and water. It involves chlorophyll and produces oxygen as a byproduct."
    
    response = client.post("/quiz", json={"text": test_text})
    assert response.status_code == 200
    data = response.json()
    assert "quiz" in data
    quiz = data["quiz"]
    assert isinstance(quiz, list)
    assert len(quiz) == 3, f"Expected 3 questions, got {len(quiz)}"
    
    for idx, q in enumerate(quiz):
        assert "question" in q, f"Question {idx} missing question field"
        assert "options" in q, f"Question {idx} missing options"
        assert "correct_answer" in q, f"Question {idx} missing correct_answer"
        assert len(q["options"]) == 4, f"Question {idx} should have 4 options"
        assert q["correct_answer"] in q["options"], f"Question {idx} correct_answer not in options"
    
    print(f"✓ Quiz module passed - generated {len(quiz)} questions, source: {data['source']}")
    
    # Test with topic only
    response = client.post("/quiz", json={"text": "Machine Learning"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["quiz"]) == 3
    print("✓ Quiz topic-only passed")
    
    # Empty should fail
    response = client.post("/quiz", json={"text": ""})
    assert response.status_code == 400
    print("✓ Quiz validation passed")

def test_summarize_endpoint():
    """Test Summary module"""
    long_text = """
    Artificial Intelligence (AI) is a broad field of computer science concerned with building smart machines capable of performing tasks that typically require human intelligence. 
    AI is an interdisciplinary science with multiple approaches, but advancements in machine learning and deep learning are creating a paradigm shift in virtually every sector of the tech industry. 
    AI systems work by ingesting large amounts of labeled training data, analyzing the data for correlations and patterns, and using these patterns to make predictions about future states. 
    In this way, a chatbot that is fed examples of text can learn to generate lifelike exchanges with people, or an image recognition tool can learn to identify and describe objects in images by reviewing millions of examples. 
    AI programming focuses on three cognitive skills: learning, reasoning and self-correction.
    """
    
    response = client.post("/summarize", json={"text": long_text})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert len(data["summary"]) > 20
    assert data["summary_length"] <= data["original_length"]
    print(f"✓ Summarize module passed - {data['original_length']} -> {data['summary_length']} chars, source: {data['source']}")
    
    # Too short should fail
    response = client.post("/summarize", json={"text": "Short"})
    assert response.status_code == 400
    print("✓ Summarize validation passed")

def test_learning_path_endpoint():
    """Test Learning Path module"""
    response = client.post("/learn/recommendations", json={"topic": "SQL"})
    assert response.status_code == 200
    data = response.json()
    assert "learning_path" in data
    assert len(data["learning_path"]) > 100
    assert "SQL" in data["learning_path"] or "sql" in data["learning_path"].lower()
    # Should contain structured levels
    assert "Beginner" in data["learning_path"] or "beginner" in data["learning_path"].lower()
    print(f"✓ Learning Path module passed - source: {data['source']}")
    
    # Empty should fail
    response = client.post("/learn/recommendations", json={"topic": ""})
    assert response.status_code == 400
    print("✓ Learning Path validation passed")

def test_all_endpoints_with_compat_routes():
    """Test compatibility routes under /api/*"""
    # These are additional routes for compatibility
    endpoints = [
        ("/api/qa", {"query": "What is AI?"}),
        ("/api/explain", {"topic": "Gravity"}),
        ("/api/quiz", {"text": "Gravity is a force that attracts objects"}),
        ("/api/summarize", {"text": "Gravity is a fundamental force of nature. It is the force that attracts a body toward the center of the earth, or toward any other physical body having mass. This is a long enough text to test summarization properly with more than fifty characters."}),
        ("/api/learn/recommendations", {"topic": "Python"}),
    ]
    
    for endpoint, payload in endpoints:
        response = client.post(endpoint, json=payload)
        assert response.status_code == 200, f"Failed for {endpoint}: {response.text}"
        print(f"✓ Compat route {endpoint} passed")

def test_error_handling():
    """Test error handling for invalid inputs"""
    # Missing field
    response = client.post("/qa", json={})
    assert response.status_code in [400, 422]
    print("✓ Error handling - missing field passed")
    
    # Invalid JSON structure
    response = client.post("/quiz", json={"text": "ab"})
    assert response.status_code == 400
    print("✓ Error handling - short input passed")

def test_gemini_fallback():
    """Test that fallback works when no API key"""
    # This test ensures app works without API key (important for testing environment)
    # All endpoints should return fallback responses if no key
    response = client.post("/qa", json={"query": "Test fallback"})
    assert response.status_code == 200
    data = response.json()
    # Should have source field indicating fallback or gemini
    assert data["source"] in ["gemini", "fallback", "no-op"]
    print(f"✓ Fallback mechanism works - source: {data['source']}")

if __name__ == "__main__":
    # Run tests manually if needed
    test_health_check()
    test_api_status()
    test_home_page()
    test_qa_endpoint()
    test_explain_endpoint()
    test_quiz_endpoint()
    test_summarize_endpoint()
    test_learning_path_endpoint()
    test_all_endpoints_with_compat_routes()
    test_error_handling()
    test_gemini_fallback()
    print("\n✅ All tests passed!")
