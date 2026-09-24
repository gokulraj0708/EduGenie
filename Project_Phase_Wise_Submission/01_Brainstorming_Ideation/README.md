# Phase 1: Brainstorming & Ideation - EduGenie

## Project Title
**EduGenie: Google Gemini Powered Learning Assistant**

## Idea Overview
EduGenie is a lightweight AI-powered educational assistant that simplifies learning through generative AI. Designed for students of all academic levels, it leverages cloud-based AI (Gemini 1.5 Pro) and local efficient models (LaMini-Flan-T5-783M) to make quality education accessible even on low-resource devices like Mac M1.

## Problem Identification

### Current Challenges in Education:
1. **Information Overload**: Students struggle with vast educational content, finding it hard to extract key points
2. **Complex Concepts**: Many topics are explained in overly technical language, difficult for beginners
3. **Lack of Personalization**: One-size-fits-all learning doesn't cater to individual pace and level
4. **Assessment Gaps**: Students lack tools to test their understanding immediately after learning
5. **Resource Scattered**: Learning resources are scattered across platforms, no structured path
6. **Accessibility**: High-quality AI learning tools often require expensive hardware

### Specific Pain Points Observed:
- Student asks "Which is the largest ocean?" - needs instant accurate answer
- Student wants to test understanding of "Pythagoras Theorem" - needs quiz generation
- Learner exploring SQL - needs structured beginner to advanced path with timelines
- Long textbook passages - need quick revision summaries

## Proposed Concept

### Core Concept:
A unified web platform with 5 AI-powered modules:
1. **QnA Module**: Instant accurate answers using Gemini 1.5 Pro
2. **Explanation Module**: Simplified explanations using LaMini-Flan-T5 + Gemini
3. **Quiz Module**: Auto-generates 3 MCQs with 4 options each in JSON format
4. **Summary Module**: Concise summaries retaining core information
5. **Learning Path Module**: Personalized structured path with resources

### Innovation:
- **Hybrid AI**: Combines cloud power (Gemini) with local efficiency (LaMini-Flan-T5)
- **Lightweight**: FastAPI + HTML/CSS - runs on low-end devices
- **Fallback System**: Works even without API key for demo/testing
- **Real Integration**: All features actually work, not mocked
- **JSON Output**: Quiz module outputs structured JSON for easy LMS integration

## Target Users

### Primary Users:
1. **School Students (Class 6-12)**: Need simplified explanations, quick QnA, quiz practice
2. **College Students**: Need learning paths for new technologies (SQL, Python, ML), summarization for research
3. **Self-Learners**: Exploring new domains, need structured guidance
4. **Competitive Exam Aspirants**: Quick revision via summaries, self-assessment via quizzes

### Secondary Users:
1. **Educators**: Can use to generate quizzes, explanations for students
2. **Content Platforms**: Can integrate API for enhanced learning experience
3. **Developers**: Lightweight codebase easy to understand and extend

## Expected Impact

### Educational Impact:
- **Democratize Learning**: Quality AI assistance accessible on any device
- **Reduce Learning Time**: Summaries and structured paths save 40-60% time
- **Improve Retention**: Immediate quiz generation improves recall by testing
- **Personalization**: Adaptive learning paths cater to individual levels

### Technical Impact:
- **Showcase AI Integration**: Real example of Gemini API + local models
- **Maintainable Architecture**: Simple enough for college students to understand and explain
- **Scalable Foundation**: Modular design allows future enhancements (voice, multilingual, mobile app)

### Social Impact:
- **Bridge Digital Divide**: Works on low-resource devices, no heavy GPU needed
- **Inclusive**: Simple UI, clear language, accessible to beginners
- **Future Ready**: Foundation for voice interaction, multilingual, LMS integration

## Initial Solution Sketch

### Architecture Overview:
```
User (Browser) → HTML/CSS Form (Task Dropdown + Textarea)
                ↓ POST /qa, /explain, /quiz, /summarize, /learn/recommendations
            FastAPI Backend → Module Logic
                            → Try Gemini 1.5 Pro API
                            → Fallback to templated logic if no key
                ↓ JSON Response
            Frontend displays result + interactive quiz
```

### Folder Architecture (from reference):
```
EduGenie/
├── main.py (FastAPI app)
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── templates/index.html
├── static/style.css
├── requirements.txt
```

### Enhanced Structure for MVP Quality:
```
PROJECT/
├── app/
│   ├── main.py
│   ├── qna.py, explanation_module.py, etc.
│   ├── templates/index.html
│   ├── static/style.css
├── tests/
├── scripts/
├── docs/screenshots, videos, additional-documentation
├── Project_Phase_Wise_Submission/ (8 phases)
```

## Brainstorming Outcomes

### Features Finalized (Mandatory):
- ✅ QnA: Smart concise answers
- ✅ Explain: Simplified explanations
- ✅ Quiz: 3 MCQs, 4 options, JSON, with correct answer validation
- ✅ Summarize: Concise versions retaining core info
- ✅ Learning Path: Beginner to advanced with timelines and resources

### Technologies Chosen:
- **Backend**: FastAPI (modern, fast, auto docs)
- **Frontend**: HTML + CSS + Vanilla JS (simple, no heavy framework)
- **Templating**: Jinja2
- **Server**: Uvicorn
- **AI**: Google Gemini 1.5 Pro (via API), LaMini-Flan-T5-783M (local fallback concept)
- **Testing**: pytest + TestClient

### Non-Goals (Future Enhancements):
- Voice-based interaction (future)
- Multilingual support (future)
- Mobile app (future)
- Progress tracking dashboard (future)
- Gamification (future)

## Conclusion
EduGenie addresses real student pain points with a simple, working, testable MVP that demonstrates genuine AI integration. It's designed to be installable, runnable, and explainable by a college student, following the engineering quality seen in ComicCraft sample repository.

---
**Phase 1 Completed**: Idea, problem, concept, users, impact, initial solution documented.
