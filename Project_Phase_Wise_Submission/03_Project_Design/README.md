# Phase 3: Project Design - EduGenie

## System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     User Layer                              │
│  Browser (Chrome/Firefox) - HTML/CSS/JS Frontend            │
│  - Task Dropdown (5 options)                                │
│  - Textarea with char count                                 │
│  - Example buttons                                          │
│  - Result container (markdown + interactive quiz)           │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP POST (JSON) / GET
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (app/main.py)              │
│  - Serves index.html via Jinja2                             │
│  - 5 Core Endpoints:                                        │
│    • POST /qa → qna.py                                      │
│    • POST /explain → explanation_module.py                  │
│    • POST /quiz → quiz_module.py                            │
│    • POST /summarize → summary_module.py                    │
│    • POST /learn/recommendations → learning_path.py         │
│  - Health: GET /health, /api/status                         │
│  - Docs: /api/docs (auto)                                   │
│  - Static: /static/style.css                                │
└──────────────────────┬──────────────────────────────────────┘
                       │ Module Logic
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI Integration Layer                      │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────┐ │
│  │ Gemini 1.5 Pro  │  │ LaMini-Flan-T5   │  │  Fallback   │ │
│  │ (via API)       │  │ (local optional) │  │  Templates  │ │
│  │ - QnA           │  │ - Explanation    │  │  - Knowledge│ │
│  │ - Quiz          │  │                  │  │  - Extractive│ │
│  │ - Summary       │  │                  │  │  - Structured│ │
│  │ - Learning Path │  │                  │  │             │ │
│  └─────────────────┘  └──────────────────┘  └─────────────┘ │
│  Config: app/config.py reads GEMINI_API_KEY from .env       │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Explanation
- **Frontend-Backend Separation**: Simple but clean separation, same origin (no CORS issues)
- **Modular Design**: Each AI feature in separate file (qna.py, explanation_module.py, etc.) for maintainability
- **Hybrid AI Strategy**: Try Gemini first (cloud power), then local model if configured, then fallback (ensures always works)
- **Fallback First**: Critical for testing/demo without API key, never claims fake success, clearly indicates source
- **Lightweight**: No heavy frameworks, FastAPI + vanilla JS, runs on M1/low-resource

## Modules Description

### 1. Config Module (app/config.py)
- **Purpose**: Centralized configuration
- **Functions**: 
  - `has_gemini_key()`: Check if API key configured
  - `get_gemini_model_name()`: Get model name from env
- **Env Vars**: GEMINI_API_KEY, GOOGLE_API_KEY, GEMINI_MODEL, USE_LOCAL_MODEL, HOST, PORT

### 2. QnA Module (app/qna.py)
- **Purpose**: Answer academic questions
- **Key Functions**:
  - `answer_question(query)`: Main function
  - `_get_fallback_answer(query)`: Fallback with knowledge base
- **Logic**:
  1. Validate input
  2. If Gemini key exists, try genai.GenerativeModel.generate_content with educational prompt
  3. If fails or no key, use fallback with keyword matching and generic template
  4. Return dict with answer, source, model, query
- **Prompt Engineering**: "You are EduGenie, educational assistant, answer concisely, student-friendly, key points, examples"

### 3. Explanation Module (app/explanation_module.py)
- **Purpose**: Simplify complex concepts
- **Key Functions**:
  - `explain_concept(topic)`: Main
  - `_fallback_explanation(topic)`: Structured template with definition, components, analogy, steps, summary
  - `_try_local_model(topic)`: Try transformers pipeline for LaMini-Flan-T5-783M if USE_LOCAL_MODEL=true
- **Logic**: Local → Gemini → Fallback
- **Prompt**: "Explain {topic} simple, clear, analogy, structure: Definition, Key Points, Analogy, Summary, 200-300 words, emojis"

### 4. Quiz Module (app/quiz_module.py)
- **Purpose**: Generate 3 MCQs with 4 options each, JSON format
- **Key Functions**:
  - `generate_quiz(text)`: Main
  - `clean_json_block(text)`: Remove ```json and ``` markers (as per reference doc)
  - `_fallback_quiz_generation(text)`: Keyword extraction + templated questions
- **Logic**:
  1. Validate input (min length)
  2. Gemini prompt expecting valid JSON array, 3 questions, 4 options, correct_answer
  3. Clean response via clean_json_block
  4. Parse JSON, validate structure (3 questions, 4 options, correct in options)
  5. If invalid/empty/fails, use fallback
  6. Return quiz list
- **Prompt**: Specifies exact JSON format, no markdown, correct_answer must match option

### 5. Summary Module (app/summary_module.py)
- **Purpose**: Summarize long passages concisely
- **Key Functions**:
  - `summarize_text(text)`: Main
  - `_fallback_summarize(text)`: Extractive summarization via keyword frequency scoring
- **Fallback Logic**:
  - Split into sentences
  - Count word frequency (filter common words)
  - Score sentences by keyword frequency, boost first/last
  - Take top 30% or 2-4 sentences, preserve order
  - Return with stats
- **Prompt**: "Summarize educational passage, retain core info, eliminate redundancy, 30-40% length, clear, student-friendly"

### 6. Learning Path Module (app/learning_path.py)
- **Purpose**: Personalized structured learning path
- **Key Functions**:
  - `get_learning_recommendations(topic)`: Main
  - `_fallback_learning_path(topic)`: Detailed templated path with 4 levels
- **Fallback Structure**:
  - Overview
  - Level 1 Beginner (Week 1-2): Topics, Resources (videos, articles, books), Milestone
  - Level 2 Intermediate (Week 3-5)
  - Level 3 Advanced (Week 6-8)
  - Level 4 Expert (Ongoing)
  - Timeline table, Tools, Study Tips, Success Metrics, Resource Links
- **Prompt**: "Generate personalized structured learning path for {topic}, beginner to advanced, topics, timeline, resources (videos, articles, books), projects, milestones, specific to topic"

### 7. Main App (app/main.py)
- **Purpose**: FastAPI app, routing, templating
- **Components**:
  - FastAPI instance with title, description, version
  - Templates (Jinja2) and Static (CSS)
  - Pydantic models for request validation (QARequest, ExplainRequest, etc. with get_* methods for compatibility)
  - Routes: GET /, /health, /api/status, POST 5 core endpoints + compat /api/*
  - Error handlers
  - Logging

## Data Flow

### QnA Flow:
```
User enters "Which is largest ocean?" in textarea, selects QnA, clicks Generate
→ JS fetch POST /qa {query: "..."}
→ FastAPI validates, calls answer_question(query)
→ answer_question checks has_gemini_key()
→ If yes: genai.configure, GenerativeModel, generate_content(prompt)
→ If response.text: return {answer, source: gemini}
→ If no key/fails: _get_fallback_answer → templated answer with knowledge base
→ FastAPI returns JSON
→ JS displayResult formats markdown, shows source badge
```

### Quiz Flow:
```
User pastes paragraph about photosynthesis, selects Quiz
→ POST /quiz {text: "..."}
→ generate_quiz validates length
→ If Gemini: prompt for 3 MCQs JSON, clean_json_block, json.loads, validate
→ If valid: return quiz list
→ If invalid/no key: _fallback_quiz_generation extracts keywords, creates 3 templated questions
→ Frontend shows count + interactive quiz with radio buttons + feedback + raw JSON details
```

### All modules follow similar pattern: Validate → Try Gemini → Fallback → Return with source indicator

## User Flow

1. **Landing**: User opens http://127.0.0.1:8000, sees header with EduGenie logo, tagline, status badge (Gemini Active or Fallback Mode)
2. **Selection**: Chooses task from dropdown (QnA, Explain, Quiz, Summarize, Learning Path) or clicks feature card or example button
3. **Input**: UI updates label and placeholder based on task, user enters text, sees char count
4. **Examples**: Can click example buttons (Largest Ocean, Pythagoras, etc.) to auto-fill
5. **Submit**: Clicks "Generate with EduGenie", sees loading spinner "EduGenie is thinking..."
6. **Result**: Result container appears below with:
   - Source badge (gemini/fallback)
   - Formatted markdown result
   - For quiz: interactive radio buttons with correct/incorrect feedback + raw JSON
   - Copy and clear buttons
7. **Iterate**: Can try other tasks, copy result, clear

## Database Design

### No Database for MVP (as per reference):
- Reference folder architecture shows no DB, just modules and templates
- This is intentional for lightweight MVP
- All processing is stateless, no persistence needed for core features
- Future enhancement could add: user history, progress tracking, saved quizzes

### If DB needed (future):
- Could use SQLite for simplicity
- Tables: users, queries, quizzes, learning_paths
- But not required for current MVP scope

## API Design

### Endpoints:

#### GET /
- **Purpose**: Serve frontend
- **Response**: HTML (index.html via Jinja2)
- **Params**: None

#### GET /health
- **Purpose**: Health check
- **Response**: JSON {status, service, version, gemini_configured, model, endpoints}

#### GET /api/status
- **Purpose**: Detailed status
- **Response**: JSON {status, service, features, gemini_configured, model, fallback_available}

#### POST /qa
- **Request**: JSON {query: string} or {question: string}
- **Response**: JSON {answer: string, source: gemini|fallback, model, query, note?}
- **Errors**: 400 empty, 500 internal

#### POST /explain
- **Request**: JSON {topic: string} or {text, concept}
- **Response**: JSON {explanation: string, source, model, topic}
- **Errors**: 400 empty

#### POST /quiz
- **Request**: JSON {text: string} or {topic, passage}
- **Response**: JSON {quiz: [{question, options[4], correct_answer, explanation}], source, model, input_text}
- **Errors**: 400 empty or too short

#### POST /summarize
- **Request**: JSON {text: string} or {passage, content}
- **Response**: JSON {summary: string, source, model, original_length, summary_length, compression_ratio}
- **Errors**: 400 empty or <50 chars

#### POST /learn/recommendations
- **Request**: JSON {topic: string} or {text}
- **Response**: JSON {learning_path: string (markdown), source, model, topic}
- **Errors**: 400 empty

#### Compat Routes:
- POST /api/qa, /api/explain, /api/quiz, /api/summarize, /api/learn/recommendations (same as above)

#### GET /api/docs
- **Purpose**: Auto-generated Swagger docs (FastAPI)

### Request/Response Examples:

**QnA Request:**
```json
{"query": "Which is the largest ocean?"}
```

**QnA Response:**
```json
{
  "answer": "The Pacific Ocean is the largest...",
  "source": "gemini",
  "model": "gemini-1.5-flash",
  "query": "Which is the largest ocean?"
}
```

**Quiz Response:**
```json
{
  "quiz": [
    {
      "question": "What is photosynthesis?",
      "options": ["Process by plants...", "...", "...", "..."],
      "correct_answer": "Process by plants...",
      "explanation": "Photosynthesis is..."
    },
    {...}, {...}
  ],
  "source": "gemini",
  "input_text": "Photosynthesis is..."
}
```

## AI Workflow

### Gemini Integration Workflow (for all modules):
1. Check has_gemini_key() - if false, skip to fallback
2. import google.generativeai, configure with API key
3. Create GenerativeModel with GEMINI_MODEL (gemini-1.5-flash default, 1.5 Pro compatible)
4. Craft detailed prompt specific to module (as described in module section)
5. Call model.generate_content(prompt)
6. If response and response.text: return with source=gemini
7. Else: log warning, use fallback
8. Exception handling: catch any error, log, use fallback with error_detail

### clean_json_block (Quiz):
- As per reference doc: "cleans any Markdown code blocks using clean_json_block function"
- Implementation: regex remove ```json, ``` markers, trim

### Fallback Workflow:
- QnA: Keyword matching + knowledge base + generic template
- Explain: Structured template with definition, components, analogy, steps
- Quiz: Keyword extraction + templated questions ensuring 3 questions, 4 options, correct in options
- Summary: Extractive via word frequency scoring
- Learning Path: Detailed 4-level templated path with timeline table, resources, tips

### Local Model (LaMini-Flan-T5) Workflow (Optional):
1. Check USE_LOCAL_MODEL env var
2. If true, try transformers pipeline
3. Try MBZUAI/LaMini-Flan-T5-783M, fallback to google/flan-t5-small
4. Generate with prompt
5. If success, return with source=local_model
6. If fails, continue to Gemini/fallback

## Security Considerations

1. **No Secrets in Code**: API keys via env vars, .env not committed, .env.example provided
2. **Input Validation**: Pydantic models, empty checks, length checks
3. **Error Handling**: No stack traces exposed to user, only useful messages, error_detail logged server-side but also returned for debugging (without secrets)
4. **No Injection**: No eval, no SQL (no DB), JSON parsing with try/except
5. **CORS**: Same origin, no need for CORS config in MVP, but could add if frontend separate
6. **Rate Limiting**: Not implemented in MVP (future: add slowapi)
7. **Logging**: Logging with logger, no sensitive data logged

## Frontend Design

### Design System:
- **Colors**: Primary #6366f1 (indigo), secondary #8b5cf6 (purple), accent #06b6d4 (cyan), success #10b981, warning #f59e0b
- **Fonts**: Inter for body, Poppins for logo/title
- **Icons**: Font Awesome 6
- **Layout**: Container max 1100px, centered, gradient background (indigo to purple)
- **Cards**: White, rounded 16px, shadow-lg
- **Responsive**: Grid for features, flex for examples, mobile breakpoint 768px

### Components:
- Header: Logo (grad cap icon + EduGenie), tagline, subtitle, status badge
- Main Card: Input section (dropdown, textarea, char count, examples, submit btn, loading), result container (header with source badge + copy/clear, content, quiz interactive), error container
- Features: 5 cards with icon, title, description, endpoint tag, clickable to select task
- Scenarios: 3 scenarios from reference doc
- Footer: Description, tech stack, links (API Docs, Health, GitHub), submission info

### JS Logic:
- taskConfig object mapping task to label, placeholder, endpoint, field
- updateUIForTask updates label/placeholder
- Example buttons fill task and text
- Feature cards select task
- Submit: validation, loading state, fetch POST, displayResult
- displayResult: formatMarkdown (basic markdown to HTML), quiz interactive with radio + feedback
- Copy/clear buttons
- Ctrl+Enter to submit

## Project Structure (Final)
```
EduGenie/
├── app/
│   ├── __init__.py
│   ├── main.py (FastAPI app)
│   ├── config.py (env config)
│   ├── qna.py
│   ├── explanation_module.py
│   ├── quiz_module.py
│   ├── summary_module.py
│   ├── learning_path.py
│   ├── templates/index.html
│   └── static/style.css
├── tests/
│   ├── __init__.py
│   ├── test_api.py (endpoint tests)
│   └── test_modules.py (unit tests)
├── scripts/
│   ├── run.py
│   └── setup.py
├── docs/
│   ├── screenshots/ (real captures)
│   ├── videos/ (demo + testing)
│   └── additional-documentation/Project_Documentation.docx
├── Project_Phase_Wise_Submission/
│   ├── 01_Brainstorming_Ideation/README.md
│   ├── 02_Requirement_Analysis/README.md
│   ├── 03_Project_Design/README.md (this file)
│   ├── 04_Project_Planning/README.md
│   ├── 05_Project_Development/README.md
│   ├── 06_Project_Testing/README.md
│   ├── 07_Project_Documentation/README.md
│   └── 08_Project_Demonstration/README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── DOC-20260921-WA0003.pdf (reference)
└── Master_MVP_Prompt_New_Project.md (master prompt)
```

---
**Phase 3 Completed**: Architecture, modules, data flow, user flow, DB, API, AI workflow, security, frontend, structure documented.
