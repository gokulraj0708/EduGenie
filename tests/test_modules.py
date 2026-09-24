"""
Unit tests for individual EduGenie modules
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.qna import answer_question
from app.explanation_module import explain_concept
from app.quiz_module import generate_quiz, clean_json_block
from app.summary_module import summarize_text
from app.learning_path import get_learning_recommendations

def test_qna_module():
    result = answer_question("Which is the largest ocean?")
    assert "answer" in result
    assert len(result["answer"]) > 10
    assert result["source"] in ["gemini", "fallback"]
    print(f"✓ QnA module unit test - {result['source']}")

def test_explanation_module():
    result = explain_concept("Photosynthesis")
    assert "explanation" in result
    assert len(result["explanation"]) > 20
    print(f"✓ Explanation module unit test - {result['source']}")

def test_quiz_module():
    result = generate_quiz("Photosynthesis is important for plants")
    assert "quiz" in result
    assert len(result["quiz"]) == 3
    for q in result["quiz"]:
        assert len(q["options"]) == 4
    print(f"✓ Quiz module unit test - {result['source']}")
    
    # Test clean_json_block function from reference doc
    test_json = "```json\n[{\"question\": \"test\"}]\n```"
    cleaned = clean_json_block(test_json)
    assert "```" not in cleaned
    print("✓ clean_json_block function test")

def test_summary_module():
    long_text = "AI is a broad field of computer science. It builds smart machines. These machines perform tasks requiring human intelligence. AI uses machine learning and deep learning. It is transforming every sector of tech industry. AI systems ingest large amounts of training data. They analyze data for patterns. They make predictions about future states."
    result = summarize_text(long_text)
    assert "summary" in result
    print(f"✓ Summary module unit test - {result['source']}")

def test_learning_path_module():
    result = get_learning_recommendations("Python Programming")
    assert "learning_path" in result
    assert "Python" in result["learning_path"] or "python" in result["learning_path"].lower()
    print(f"✓ Learning Path module unit test - {result['source']}")

def test_edge_cases():
    # Empty inputs
    assert "error" in answer_question("")
    assert "error" in explain_concept("")
    assert "error" in generate_quiz("")
    assert "error" in summarize_text("")
    assert "error" in get_learning_recommendations("")
    print("✓ Edge cases - empty inputs handled")
    
    # Short inputs for summary
    result = summarize_text("Short text")
    assert "error" in result
    print("✓ Edge cases - short text validation")

if __name__ == "__main__":
    test_qna_module()
    test_explanation_module()
    test_quiz_module()
    test_summary_module()
    test_learning_path_module()
    test_edge_cases()
    print("\n✅ All module unit tests passed!")
