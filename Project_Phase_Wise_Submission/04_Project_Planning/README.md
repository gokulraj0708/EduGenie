# Phase 4: Project Planning - EduGenie

## Development Plan

### Approach: Agile with MVP Focus
- **Goal**: Build real, working, tested MVP from scratch, not mock
- **Inspired by**: ComicCraft sample repo organization, but independent design per EduGenie reference
- **Principle**: Simple, maintainable, runnable by college student, real functionality only

### Phases Breakdown (8 Phases, No Phase 9):

#### Phase 1: Brainstorming & Ideation (Completed)
- Study reference document (17 pages PDF)
- Extract title, scenario, problem, objectives, modules, features, tech stack
- Identify target users, impact, initial solution
- Inspect ComicCraft sample for engineering quality (structure, tests, docs, screenshots)

#### Phase 2: Requirement Analysis (Completed)
- Problem statement, objectives
- Functional requirements (5 modules + frontend + backend)
- Non-functional (performance, reliability, usability, maintainability, security, compatibility)
- User requirements (student, developer/reviewer)
- Software/hardware requirements
- AI/API requirements (Gemini, LaMini-Flan-T5)
- Constraints, assumptions, expected outputs

#### Phase 3: Project Design (Completed)
- System architecture (high-level diagram, explanation)
- Modules description (config, qna, explanation, quiz, summary, learning_path, main)
- Data flow (example QnA and Quiz flows)
- User flow (landing → selection → input → submit → result)
- Database design (no DB for MVP, future scope)
- API design (endpoints, request/response examples)
- AI workflow (Gemini integration, clean_json_block, fallback, local model)
- Security considerations
- Frontend design (design system, components, JS logic)
- Project structure

#### Phase 4: Project Planning (Current)
- Development plan, module-wise tasks, testing plan, documentation plan, demonstration plan, milestones

#### Phase 5: Project Development
- Actual implementation: setup, frontend, backend, AI integration, validation, error handling

#### Phase 6: Project Testing
- Test strategy, test cases, automated tests, manual testing, results, bug fixes

#### Phase 7: Project Documentation
- README, DOCX with screenshots, phase docs, links

#### Phase 8: Project Demonstration
- Demo workflow, key features, final output, videos, links

## Module-Wise Tasks

### Module 1: Project Setup & Configuration
- **Tasks**:
  - Create folder structure (app/, tests/, scripts/, docs/, Project_Phase_Wise_Submission/)
  - Create requirements.txt with pinned versions
  - Create .env.example and .gitignore
  - Create app/__init__.py, app/config.py with env handling
  - Setup logging
- **Estimated Time**: 1 hour
- **Dependencies**: None
- **Output**: Runnable skeleton, config works

### Module 2: QnA Module (app/qna.py)
- **Tasks**:
  - Implement _get_fallback_answer with knowledge base (ocean, river, pythagoras, sql)
  - Implement answer_question with Gemini try/except and fallback
  - Prompt engineering for educational QnA
  - Test with sample queries
- **Time**: 1.5 hours
- **Dependencies**: config.py
- **Output**: Working QnA with fallback

### Module 3: Explanation Module (app/explanation_module.py)
- **Tasks**:
  - Implement _fallback_explanation templated structure
  - Implement _try_local_model with transformers pipeline (optional)
  - Implement explain_concept with local → Gemini → fallback
  - Prompt for simplified explanation
- **Time**: 1.5 hours
- **Dependencies**: config.py
- **Output**: Working explanation module

### Module 4: Quiz Module (app/quiz_module.py)
- **Tasks**:
  - Implement clean_json_block as per reference doc
  - Implement _fallback_quiz_generation with keyword extraction
  - Implement generate_quiz with Gemini JSON prompt, validation (3 Qs, 4 options, correct in options)
  - Test JSON parsing and validation
- **Time**: 2 hours (critical, JSON handling tricky)
- **Dependencies**: config.py
- **Output**: Working quiz generator

### Module 5: Summary Module (app/summary_module.py)
- **Tasks**:
  - Implement _fallback_summarize extractive via word frequency
  - Implement summarize_text with Gemini abstractive prompt
  - Handle short text (<200 chars) no-op case
  - Compression stats
- **Time**: 1.5 hours
- **Dependencies**: config.py
- **Output**: Working summarizer

### Module 6: Learning Path Module (app/learning_path.py)
- **Tasks**:
  - Implement _fallback_learning_path detailed 4-level structure
  - Implement get_learning_recommendations with Gemini prompt
  - Ensure markdown formatting with emojis, tables
- **Time**: 1.5 hours
- **Dependencies**: config.py
- **Output**: Working learning path generator

### Module 7: FastAPI Backend (app/main.py)
- **Tasks**:
  - Create FastAPI app with metadata
  - Setup Jinja2 templates and static files
  - Create Pydantic models with get_* methods for compatibility
  - Implement GET /, /health, /api/status
  - Implement POST /qa, /explain, /quiz, /summarize, /learn/recommendations
  - Implement compat routes /api/*
  - Error handlers, logging
  - Test with TestClient
- **Time**: 2 hours
- **Dependencies**: All 5 modules
- **Output**: Working API server

### Module 8: Frontend (templates/index.html, static/style.css)
- **Tasks**:
  - Design HTML structure: header, main card (input, result, error), features, scenarios, footer
  - Create CSS: design system, responsive, gradient, cards, animations
  - Implement JS: taskConfig, updateUIForTask, examples, feature cards, submit with fetch, displayResult with markdown formatting and quiz interactive
  - Test in browser
- **Time**: 3 hours
- **Dependencies**: Backend
- **Output**: Working responsive frontend

### Module 9: Testing (tests/)
- **Tasks**:
  - Create tests/test_api.py with endpoint tests (health, home, 5 modules, compat, error handling, fallback)
  - Create tests/test_modules.py with unit tests for each module
  - Run pytest, fix failures
  - Manual browser testing of UI workflows
- **Time**: 2 hours
- **Dependencies**: Backend + Frontend
- **Output**: Passing tests, test results documented

### Module 10: Documentation & Screenshots
- **Tasks**:
  - Create README.md with project info, features, tech stack, install, run, test, screenshots, etc.
  - Capture real screenshots from running app (01_home, 02_qa, 03_explain, 04_quiz, 05_summary, 06_learning_path, 07_api_docs)
  - Create docs/additional-documentation/Project_Documentation.docx with embedded screenshots (using python-docx)
  - Create phase-wise README.md for all 8 phases
- **Time**: 3 hours
- **Dependencies**: Working app + tests
- **Output**: Docs, screenshots, DOCX

### Module 11: Videos (Demo + Testing)
- **Tasks**:
  - Prepare voice options: 2 male college-student voices with Indian English accent via add_voice tool
  - Let user select voice
  - Create demo video script (2-4 min): intro, UI, 5 features demo with realistic input, architecture explanation, conclusion
  - Create testing video script (2-4 min): VS Code structure, tests/, run pytest, show output, manual validation, conclusion
  - Use selected voice for both videos via generate_speech
  - Attempt screen recording, if unavailable provide narration/script and steps honestly
- **Time**: 2 hours (depends on recording availability)
- **Dependencies**: Voice selection, working app
- **Output**: Videos or honest report + scripts

### Module 12: Final Checks & GitHub
- **Tasks**:
  - Verify project files, remove unnecessary
  - Check for secrets (no .env, no API keys)
  - Run tests again
  - Verify README, screenshots, DOCX, phases
  - Commit meaningful changes
  - Push to GitHub branch arena/01a0d350-edugenie
- **Time**: 1 hour
- **Dependencies**: All above
- **Output**: Clean repo pushed

## Testing Plan

### Automated Testing:
- **Framework**: pytest + FastAPI TestClient + httpx
- **Test Files**:
  - tests/test_api.py: Endpoint tests (health, status, home, qna, explain, quiz, summary, learning_path, compat, error handling, fallback)
  - tests/test_modules.py: Unit tests for each module + edge cases + clean_json_block
- **Commands**:
  - `pytest tests/ -v` (verbose)
  - `pytest tests/test_api.py::test_qa_endpoint -v` (single)
- **Expected**: All tests pass, including fallback when no API key
- **Coverage**: At least test all 5 core endpoints, validation, error handling

### Manual Testing:
1. **Install**: pip install -r requirements.txt
2. **Configure**: Copy .env.example to .env, optionally add GEMINI_API_KEY
3. **Run**: uvicorn app.main:app --reload, open http://127.0.0.1:8000
4. **UI Workflows**:
   - Test each task dropdown option with example inputs
   - Test example buttons
   - Test feature cards
   - Test quiz interactive (select options, see feedback)
   - Test copy/clear buttons
   - Test char count
   - Test responsive (resize window)
5. **API Testing**:
   - Open /api/docs, try each endpoint
   - Test with curl or Postman
   - Test validation (empty inputs)
6. **Error Handling**:
   - No API key → should show fallback mode badge and work
   - Invalid inputs → graceful error messages
   - Network failure → fallback (if Gemini fails)

### Bug Fixing:
- If tests fail, fix code, rerun
- If UI broken, fix HTML/CSS/JS
- If fallback not working, fix templated logic
- Document bugs fixed in Phase 6

## Documentation Plan

### README.md:
- Title, description, problem, objectives, features, tech stack, architecture, workflow, installation, configuration, running, testing, screenshots, documentation, demo info, limitations, future enhancements

### DOCX (docs/additional-documentation/Project_Documentation.docx):
- Sections as per master prompt: Title Page, Description, Scenario, Problem, Need, Objectives, System Requirements, Software, Hardware, Tech Stack, Architecture, Explanation, Modules, AI Workflow, Data Flow, Features, User Flow, Project Structure, API Docs, Setup, Env Config, Execution, Testing, Test Results, Advantages, Limitations, Future, Conclusion, Screenshots with Explanation, Mandatory Functionalities, Links
- Embed real screenshots using python-docx
- Use python-docx to create

### Phase-wise Docs:
- Each phase folder has README.md with detailed project-specific content (not filler)
- Exactly 8 phases, no Phase 9

### Screenshots:
- Store in docs/screenshots/
- Naming: 01_home.png, 02_qa.png, 03_explain.png, 04_quiz.png, 05_summary.png, 06_learning_path.png, 07_api_docs.png, etc.
- Real captures from running app (use browser screenshot or playwright)

## Demonstration Plan

### Demo Video (2-4 min):
- **Structure**:
  1. Intro (15 sec): "Hi, I'm presenting EduGenie, Google Gemini Powered Learning Assistant..."
  2. Show running app in browser (10 sec)
  3. Demo QnA with "Which is largest ocean?" (20 sec)
  4. Demo Explain with "Pythagoras Theorem" (20 sec)
  5. Demo Quiz with photosynthesis text (30 sec) - show interactive
  6. Demo Summarize with long AI paragraph (20 sec)
  7. Demo Learning Path with "SQL" (20 sec)
  8. Architecture/AI workflow brief (20 sec): FastAPI, 5 modules, Gemini + fallback, clean_json_block
  9. Key features recap (10 sec)
  10. Conclusion (10 sec)
- **Voice**: Selected male Indian English college-student voice, conversational, clear, moderate speed, non-robotic
- **Recording**: Attempt screen recording with audio narration, if unavailable provide script and steps

### Testing Video (2-4 min):
- **Structure**:
  1. Intro (10 sec): "This is testing video for EduGenie..."
  2. Show VS Code project structure (15 sec): app/, tests/, etc.
  3. Show tests/ folder (10 sec): test_api.py, test_modules.py
  4. Run pytest command in terminal (30 sec): `pytest tests/ -v`, show real output
  5. Explain what is tested (30 sec): 5 modules, validation, fallback
  6. Show actual results (15 sec): passing tests
  7. Manual browser validation (20 sec): open app, test one workflow
  8. Conclusion (10 sec)
- **Voice**: Same as demo video (consistency requirement)
- **Recording**: Same handling as demo

### Voice Selection Requirement (from master prompt):
- Prepare 2 suitable male college-student voice options with Indian English accent, natural, conversational, clear, moderate speed, student-age, non-robotic
- Present as sample/preview, let user select
- Do not auto-lock before user selects
- After selection, use same voice for both videos
- If user asks agent to choose automatically, select most natural Indian male college-student presentation voice

## Milestones

| Milestone | Tasks | Timeline | Deliverable |
|-----------|-------|----------|-------------|
| M1: Setup & Modules | Setup + 5 AI modules | Day 1 Morning | Working modules with fallback |
| M2: Backend & Frontend | FastAPI + HTML/CSS/JS | Day 1 Afternoon | Working app at localhost:8000 |
| M3: Testing | Automated + manual | Day 1 Evening | Passing tests, manual validation |
| M4: Documentation | README, phases, DOCX, screenshots | Day 2 Morning | Docs, screenshots |
| M5: Videos | Voice selection, demo, testing videos | Day 2 Afternoon | Videos + narration scripts |
| M6: Final | Checks, GitHub push, final report | Day 2 Evening | Pushed repo, final report |

## Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| No Gemini API key | High | Medium | Fallback ensures app works, clearly documented |
| Gemini API failure | Medium | Medium | Try/except + fallback, graceful error |
| Quiz JSON parsing fails | Medium | High | clean_json_block + validation + fallback |
| Video recording unavailable | High | Medium | Honest report + provide scripts + steps, no fake video |
| Tests fail | Medium | High | Fix immediately, rerun, document |
| Screenshots not real | Low | High | Capture from actual running app, no AI-generated fake |

## Resources

- **Reference Document**: DOC-20260921-WA0003.pdf (17 pages, primary source)
- **Sample Repo**: https://github.com/gokulraj0708/ComicCraft (for organization, not code copying)
- **Gemini API**: https://aistudio.google.com/app/apikey
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Python**: 3.10+

---
**Phase 4 Completed**: Development plan, module tasks, testing plan, documentation plan, demonstration plan, milestones, risks documented.
