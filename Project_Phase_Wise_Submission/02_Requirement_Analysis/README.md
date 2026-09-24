# Phase 2: Requirement Analysis - EduGenie

## Problem Statement
Students across academic levels face challenges in accessing personalized, simplified, and interactive learning support. Existing solutions are either too complex, require expensive hardware, lack interactivity (no quiz generation), or provide generic unpersonalized content. There is a need for a lightweight, AI-powered educational assistant that can:

- Provide instant accurate answers to academic questions
- Simplify complex concepts into beginner-friendly language
- Generate self-assessment quizzes from any topic/passage
- Summarize long educational content for quick revision
- Offer structured personalized learning paths from beginner to advanced

The solution must work on low-resource devices (like Mac M1), be easy to install/run by college students, and demonstrate real AI integration (not mocked).

## Objectives

### Primary Objectives:
1. Build a working MVP with 5 core AI modules as per reference document
2. Integrate Google Gemini 1.5 Pro API for QnA, Quiz, Summary, Learning Path
3. Implement Explanation module with LaMini-Flan-T5-783M concept + Gemini fallback
4. Create FastAPI backend with 5 RESTful endpoints: /qa, /explain, /quiz, /summarize, /learn/recommendations
5. Develop simple responsive frontend with task dropdown, textarea, submit button, real-time result display
6. Ensure real functionality - no fake buttons, no hardcoded fake responses
7. Implement fallback logic for demo/testing without API key
8. Achieve engineering quality similar to ComicCraft sample (clean structure, tests, docs, screenshots, videos)

### Secondary Objectives:
1. Comprehensive testing (automated + manual)
2. Real screenshots from running application
3. Editable DOCX documentation with embedded screenshots
4. Demo and Testing videos (2-4 min each) with Indian English male student voice
5. 8-phase submission structure with no Phase 9
6. Professional README with setup/run instructions

## Functional Requirements

### FR1: QnA Module (/qa)
- **Input**: User question (text)
- **Process**: Send to Gemini 1.5 Pro with educational prompt, or fallback knowledge base
- **Output**: Smart concise answer, student-friendly, with source indicator
- **Validation**: Empty query rejected, min length check
- **Example**: "Which is the largest ocean?" → Pacific Ocean explanation

### FR2: Explanation Module (/explain)
- **Input**: Concept/topic name
- **Process**: Try local LaMini-Flan-T5 if configured, else Gemini with simplification prompt, else templated fallback
- **Output**: Simplified explanation with definition, key points, analogy, summary
- **Validation**: Empty topic rejected
- **Example**: "Pythagoras Theorem" → Simple breakdown with analogy

### FR3: Quiz Module (/quiz)
- **Input**: Text passage or topic
- **Process**: Gemini generates 3 MCQs, 4 options each, correct answer, JSON format. Clean markdown code blocks via clean_json_block function. Fallback generates templated quiz.
- **Output**: JSON array with 3 questions, each: question, options[4], correct_answer, explanation
- **Validation**: Input min length, ensure correct_answer in options, 3 questions
- **Example**: Input paragraph about photosynthesis → 3 MCQs
- **Special**: Interactive UI with radio buttons and correct/incorrect feedback

### FR4: Summary Module (/summarize)
- **Input**: Long educational passage (min 50 chars)
- **Process**: Gemini abstractive summarization retaining core info, eliminating redundancy. Fallback uses extractive method (keyword frequency scoring)
- **Output**: Concise summary (30-40% length), with compression stats
- **Validation**: Min 50 chars, if <200 chars return as-is with note
- **Example**: Long AI paragraph → concise version

### FR5: Learning Path Module (/learn/recommendations)
- **Input**: Topic name
- **Process**: Gemini generates personalized structured path: beginner to advanced, topics, timelines, resources (videos, articles, books), projects, milestones. Fallback provides templated path.
- **Output**: Structured markdown with levels, timeline table, resources, study tips
- **Validation**: Empty topic rejected
- **Example**: "SQL" → Beginner (Week 1-2) → Intermediate → Advanced → Expert with resources

### FR6: Frontend
- **Task Dropdown**: Explain, QnA, Quiz, Summary, Recommend Path
- **Textarea**: User input with char count
- **Submit Button**: POST to FastAPI backend
- **Result Container**: Real-time display below input, formatted markdown, quiz interactive
- **Examples**: Clickable example buttons for each task
- **Features Grid**: Clickable cards to select task
- **Responsive Design**: Works on mobile/desktop
- **Status Badge**: Shows Gemini Active or Fallback Mode

### FR7: Backend API
- **Framework**: FastAPI
- **Endpoints**: 5 core + health + status + compat /api/* routes
- **Docs**: Auto-generated at /api/docs
- **Error Handling**: Graceful handling for invalid input, API failure, missing env vars
- **CORS**: Should allow frontend (if needed, but same origin in this MVP)

## Non-Functional Requirements

### NFR1: Performance
- API response < 5 seconds for fallback, < 10 seconds for Gemini (depends on API)
- Frontend load < 2 seconds
- Lightweight, works on Mac M1, 4GB RAM

### NFR2: Reliability
- Fallback ensures app works even without API key
- No crash on invalid input, graceful error messages
- 90%+ test coverage for critical paths

### NFR3: Usability
- Simple UI understandable by school students
- Clear labels, examples, and feedback
- No technical jargon in UI
- Responsive on mobile

### NFR4: Maintainability
- Clean code, modular structure (one file per module)
- Type hints, docstrings
- Requirements.txt with pinned versions
- .env.example for configuration

### NFR5: Security
- No hardcoded secrets, use env vars
- .env not committed, .gitignore
- No exposure of API keys in logs or responses
- Input validation to prevent injection

### NFR6: Compatibility
- Python 3.10+
- Works on Windows, Mac, Linux
- Modern browsers (Chrome, Firefox, Safari)

## User Requirements

### Student User:
- As a student, I want to ask questions and get instant answers so I can clear doubts quickly
- As a student, I want complex topics explained simply so I can understand fundamentals
- As a student, I want quizzes generated from topics so I can test my understanding
- As a student, I want long passages summarized so I can revise quickly
- As a student, I want learning paths for new topics so I know what to study and in what order

### Developer/Reviewer User:
- As a reviewer, I want to run app with single command (uvicorn main:app --reload)
- As a reviewer, I want clear README with setup steps
- As a reviewer, I want automated tests that actually pass
- As a reviewer, I want real screenshots and videos, not fake

## Software Requirements

### Mandatory:
- Python 3.10+
- FastAPI 0.115.0
- Uvicorn[standard] 0.30.6
- Jinja2 3.1.4
- Python-multipart 0.0.9
- Python-dotenv 1.0.1
- Google-generativeai 0.8.3 (for Gemini)
- Pydantic 2.9.2
- Pytest 8.3.2, httpx 0.27.2 (for testing)
- HTML & CSS (frontend)
- Jinja2 templating

### Optional:
- Transformers library (for local LaMini-Flan-T5, if USE_LOCAL_MODEL=true)
- Torch (for local model)

### Tools:
- VS Code or any IDE
- Browser (Chrome recommended)
- Git & GitHub

## Hardware Requirements

### Minimum:
- CPU: Dual-core, 2GHz
- RAM: 4GB
- Storage: 500MB free
- Internet: For Gemini API (fallback works offline)

### Recommended:
- CPU: Quad-core, M1 or equivalent
- RAM: 8GB
- Storage: 1GB
- Internet: Stable for AI features

### Original Reference Spec:
- Works well on Mac M1 (lightweight, cloud-based AI)
- No heavy GPU required (uses cloud inference for Gemini, CPU-compatible LaMini-Flan-T5)

## AI/API Requirements

### Google Gemini API:
- **Model**: Gemini 1.5 Pro (or gemini-1.5-flash as efficient alternative)
- **Key**: From https://aistudio.google.com/app/apikey
- **Env Var**: GEMINI_API_KEY or GOOGLE_API_KEY
- **Usage**:
  - QnA: Prompt for concise student-friendly answer
  - Explain: Prompt for simplified explanation with analogy
  - Quiz: Prompt for 3 MCQs JSON, clean_json_block for parsing
  - Summarize: Prompt for concise version retaining core info
  - Learning Path: Prompt for structured beginner to advanced plan
- **Fallback**: If no key or API fails, use templated logic (clearly documented, not claiming fake success)

### LaMini-Flan-T5-783M (Local):
- **Purpose**: Concept explanation (lightweight, CPU-compatible, instruction-tuned)
- **Implementation**: Try transformers pipeline if USE_LOCAL_MODEL=true and library available
- **Fallback**: If not available, use Gemini or templated fallback
- **Benefits**: Local efficiency, concise context-aware responses

## Constraints

1. **Time**: MVP must be built quickly, simple architecture preferred
2. **API Key**: May not be available in testing environment - must have fallback
3. **No Fake Functionality**: Every button must work, no mocked responses claimed as real
4. **College Student Level**: Must be installable, runnable, explainable by college student
5. **Video Recording**: Environment may not support screen recording - need to handle honestly

## Assumptions

1. User has basic Python knowledge to run pip install and uvicorn
2. Internet available for Gemini API (but app works offline in fallback)
3. Browser supports modern JS (fetch API)
4. Gemini API has generous free tier for educational use
5. Fallback responses are acceptable for demo/testing when no API key
6. Simple HTML+CSS frontend is sufficient (no need for React/Vue for MVP)
7. JSON output for quiz is desired for easy integration (as per reference doc)

## Expected Outputs

1. **Working Application**: FastAPI app running at http://127.0.0.1:8000
2. **5 Functional Modules**: All endpoints working with real logic
3. **Frontend**: Responsive UI with real-time results
4. **Tests**: Automated pytest suite with actual execution results
5. **Screenshots**: Real captures from running app in docs/screenshots/
6. **Documentation**: DOCX with embedded screenshots, README.md
7. **Videos**: Demo (2-4 min) and Testing (2-4 min) with same male Indian English voice
8. **8 Phases**: Complete phase-wise submission, no Phase 9
9. **GitHub**: Clean repo with no secrets, pushed to assigned branch

---
**Phase 2 Completed**: Problem, objectives, functional/non-functional, user, software/hardware, AI/API, constraints, assumptions documented.
