# Master MVP Prompt — Build a New Academic Project from Scratch

## ROLE

Act as a senior full-stack developer, AI engineer, QA engineer, technical documentation writer, and Git/GitHub project maintainer.

Build a **real, working, tested MVP project from scratch** using the attached project-specific reference document.

Do not create a mock project, static prototype, fake API, fake screenshots, fake test results, or invented functionality.

---

## 1. SOURCE PRIORITY

### PRIMARY SOURCE — Attached Project Reference Document

The attached reference document is the **primary source of truth**.

Read the complete document before implementation and extract:

- Project title
- Scenario
- Problem statement
- Need
- Objectives
- Functional requirements
- Non-functional requirements
- Mandatory functionalities
- Software and hardware requirements
- Technologies
- Architecture
- Modules
- Features
- User flow
- Data flow
- Database requirements
- AI/API requirements
- Expected outputs
- Testing requirements
- Documentation requirements
- Demonstration requirements

Do not silently replace documented requirements with generic assumptions.

If the document does not specify something, choose a simple, reliable implementation and document the assumption.

---

## 2. SECONDARY SOURCE — COMICCRAFT SAMPLE REPOSITORY

Use this repository only as a **sample/reference for organization, engineering quality, testing, documentation, and completeness**:

**https://github.com/gokulraj0708/ComicCraft**

ComicCraft is a completed project. It is **NOT** the requirements source for the new project.

Do **not** blindly copy:

- Source code
- Features
- UI
- Architecture
- Database design
- AI workflow
- ComicCraft-specific technologies
- Project content

Instead, inspect it for useful practices such as:

- Clean repository organization
- `app/`, `tests/`, `scripts/`, `docs/`
- Real automated testing
- Real screenshots
- Editable documentation
- README quality
- `.env.example`
- Git/GitHub workflow
- 8-phase submission structure
- Practical setup/run instructions

The new project must be independently designed according to its own reference document.

---

## 3. FIRST STEP — STUDY BEFORE CODING

Before writing implementation code:

1. Read the complete attached reference document.
2. Inspect the ComicCraft sample repository.
3. Create a project requirement checklist.
4. Identify mandatory and optional features.
5. Identify required technologies.
6. Identify expected outputs.
7. Identify documentation and demonstration deliverables.
8. Decide the simplest reliable architecture.

Do not start coding before understanding the requirements.

---

## 4. BUILD THE PROJECT FROM SCRATCH

Create a genuine working MVP.

Implement the actual components required by the reference document, such as:

- Frontend/UI
- Backend
- APIs
- Database
- Authentication/authorization
- AI integration
- External APIs
- File handling
- Export/download
- Business logic
- Validation
- Error handling

Only include components relevant to the project.

Prefer a simple, maintainable architecture that can actually be installed, run, tested, demonstrated, and explained by a college student.

---

## 5. REAL FUNCTIONALITY REQUIREMENT

Every major feature shown in the UI must actually work.

Do NOT use:

- Fake buttons
- Hardcoded fake API responses
- Fake generated content
- Fake success messages
- Static screenshots presented as real output
- Mock test results
- Invented database records
- Fake AI responses
- Fake external API results

If credentials are required, use environment variables and provide `.env.example`.

If a service cannot be used because credentials are unavailable, use a clearly documented fallback only when technically appropriate. Never claim an unavailable service was successfully used.

---

## 6. RECOMMENDED PROJECT STRUCTURE

Adapt this structure to the actual technology:

```text
PROJECT/
├── app/
├── tests/
├── scripts/
├── docs/
│   ├── screenshots/
│   ├── videos/
│   └── additional-documentation/
├── Project_Phase_Wise_Submission/
│   ├── 01_Brainstorming_Ideation/
│   ├── 02_Requirement_Analysis/
│   ├── 03_Project_Design/
│   ├── 04_Project_Planning/
│   ├── 05_Project_Development/
│   ├── 06_Project_Testing/
│   ├── 07_Project_Documentation/
│   └── 08_Project_Demonstration/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
└── other project-specific files
```

Adapt it when the technology requires a different layout.

---

## 7. EXACTLY 8 PROJECT PHASES

Create exactly these eight phases:

1. **Brainstorming & Ideation**
2. **Requirement Analysis**
3. **Project Design**
4. **Project Planning**
5. **Project Development**
6. **Project Testing**
7. **Project Documentation**
8. **Project Demonstration**

There must be **NO Phase 9**.

Each phase must contain meaningful, project-specific content. Do not use filler.

### Phase 1 — Brainstorming & Ideation
Include the idea, problem identification, proposed concept, target users, expected impact, and initial solution.

### Phase 2 — Requirement Analysis
Include problem statement, objectives, functional/non-functional requirements, user requirements, software/hardware requirements, AI/API requirements where applicable, constraints, and assumptions.

### Phase 3 — Project Design
Include architecture, modules, components, data flow, user flow, database design where applicable, API design where applicable, AI workflow where applicable, and security considerations.

### Phase 4 — Project Planning
Include development plan, module-wise tasks, testing plan, documentation plan, demonstration plan, and milestones.

### Phase 5 — Project Development
Document actual setup and implementation: frontend, backend, APIs, database, AI integration, core functionality, validation, error handling, and configuration as applicable.

### Phase 6 — Project Testing
Include test strategy, test cases, automated tests, manual testing, integration testing where applicable, actual execution results, bug fixes, and final validation.

### Phase 7 — Project Documentation
Include the required project documentation and supporting materials. Avoid unnecessary duplication with the standalone documentation package.

### Phase 8 — Project Demonstration
Include the demo workflow, key features, final output, demo video, testing video, and final links.

---

## 8. TESTING — ACTUALLY TEST THE PROJECT

After implementation:

1. Install dependencies.
2. Configure the environment.
3. Start the application.
4. Verify it launches.
5. Run the actual automated test suite.
6. Test important APIs.
7. Test important UI workflows.
8. Test required integrations.
9. Test validation and error handling.
10. Fix discovered issues.
11. Run tests again.
12. Perform final manual verification.

Use the project's actual testing command. Do not assume a framework without checking the project.

Never fabricate test counts, passing tests, coverage, API responses, browser results, or performance numbers.

---

## 9. REAL SCREENSHOTS

Capture screenshots from the **actual running application**.

Never use AI-generated or mock screenshots as proof.

Store them under:

```text
docs/screenshots/
```

Use meaningful names, for example:

```text
01_home.png
02_input.png
03_processing.png
04_result.png
05_final_output.png
```

Only include screenshots that were actually captured from the running project.

---

## 10. STANDALONE EDITABLE DOCUMENTATION

Create a separate editable DOCX:

```text
docs/additional-documentation/Project_Documentation.docx
```

Embed actual screenshots directly inside the DOCX.

Include relevant sections such as:

1. Title Page
2. Project Description
3. Scenario
4. Problem Statement
5. Need for the Project
6. Objectives
7. System Requirements
8. Software Requirements
9. Hardware Requirements
10. Technology Stack
11. System Architecture
12. Architecture Explanation
13. Module Description
14. AI/API Workflow where applicable
15. Data Flow
16. Features
17. User Flow
18. Project Structure
19. API Documentation where applicable
20. Setup and Installation
21. Environment Configuration
22. Project Execution
23. Testing
24. Actual Test Results
25. Advantages
26. Limitations
27. Future Enhancements
28. Conclusion
29. Output Screenshots with Explanation
30. Mandatory/Core Functionalities
31. Project Links

Do not add irrelevant sections.

Do not invent technologies, features, results, or architecture.

---

## 11. README

Create a professional `README.md` containing only facts supported by the implementation.

Include, where applicable:

- Project title
- Description
- Problem statement
- Objectives
- Features
- Tech stack
- Architecture
- Workflow
- Installation
- Configuration
- Running instructions
- Testing
- Screenshots
- Documentation
- Demo information
- Limitations
- Future enhancements

---

## 12. DEMO VIDEO

Create a real demonstration video of approximately **2–4 minutes**.

It must:

1. Start from the actual running application in a browser.
2. Show the real UI.
3. Enter realistic input.
4. Execute the actual workflow.
5. Show the actual result.
6. Briefly explain important architecture/AI workflow.
7. Demonstrate key features.
8. End with a short conclusion.

### Voice selection requirement

For the Demo Video, first prepare **2 suitable male college-student voice options**.

The two options should both have:

- Indian English accent
- Natural pronunciation
- Conversational tone
- Clear delivery
- Moderate speaking speed
- Student-age impression
- Non-robotic presentation style

Present the **2 voice options as a sample/preview** and let the user select one.

**Do not automatically lock a voice before the user selects one.**

After the user selects the voice:

- Use the selected voice for the complete Demo Video.
- Keep the same voice identity throughout the video.
- Do not switch voices midway.
- Use the selected voice as the master voice for the Testing Video as well.

If the environment/workflow supports an explicit "best voice" selection step and the user asks the agent to choose automatically, select the voice that most naturally matches a real Indian male college-student project presentation, then continue with that same voice.

The voice should sound like a student presenting his own project, not a corporate advertisement or robotic AI narration.

---

## 13. TESTING VIDEO

Create a separate real testing video of approximately **2–4 minutes**.

It must:

1. Start from VS Code or the actual development environment.
2. Show the project structure.
3. Show `tests/`.
4. Run the actual test command.
5. Show the real terminal output.
6. Explain what is being tested.
7. Show actual results.
8. Optionally demonstrate manual browser validation.
9. End with a short conclusion.

### Voice consistency requirement

Use the **exact same voice selected for the Demo Video**.

The Testing Video must use:

- Same voice identity
- Same Indian English accent
- Same pitch
- Same age impression
- Same pronunciation
- Same speaking style

Do not select a second/different voice for the Testing Video.

Do not fabricate terminal output.

---

## 14. VIDEO HONESTY

Only create videos if the environment actually supports real screen/video recording.

If recording is unavailable, **do not fabricate a video**.

Instead, clearly report that recording is unavailable and provide the prepared narration/script and exact recording steps.

Never claim a video was recorded when it was not.

---

## 15. ENVIRONMENT VARIABLES AND SECRETS

Use environment variables for API keys, database credentials, AI credentials, external service tokens, and sensitive configuration.

Create:

```text
.env.example
```

Never commit real secrets.

Perform a final repository secret check.

---

## 16. ERROR HANDLING

Handle expected failures gracefully, including where applicable:

- Invalid input
- Missing required fields
- API failure
- AI service failure
- Database failure
- Network failure
- Missing environment variables
- File errors
- Invalid data

Provide useful user-facing messages without exposing secrets or unnecessary stack traces.

---

## 17. DOCUMENTATION MUST MATCH IMPLEMENTATION

Before finalizing, compare documentation with the actual source code.

Verify:

- Features
- Technologies
- APIs
- Database
- AI models
- Screenshots
- Test results
- Commands
- Project structure
- Limitations
- Demo workflow

Remove anything not supported by the actual implementation.

---

## 18. GITHUB WORKFLOW

Use the assigned GitHub repository for the new project.

Before pushing:

1. Verify project files.
2. Remove unnecessary files.
3. Check for secrets.
4. Run tests.
5. Verify README.
6. Verify screenshots.
7. Verify DOCX.
8. Verify phase folders.
9. Verify videos or clearly marked recording status.
10. Commit meaningful changes.
11. Push to GitHub.

Prefer a safe branch/PR workflow where possible.

Do not overwrite unrelated projects or repositories.

---

## 19. FINAL CHECKLIST

### Requirements
- [ ] Reference document completely studied
- [ ] Mandatory requirements implemented
- [ ] No unsupported features claimed

### Application
- [ ] Application starts successfully
- [ ] Main workflow works
- [ ] UI works
- [ ] Backend works
- [ ] APIs work where applicable
- [ ] Database works where applicable
- [ ] AI/API integration works where applicable
- [ ] Error handling works

### Testing
- [ ] Automated tests created
- [ ] Tests actually executed
- [ ] Failures fixed where possible
- [ ] Final result recorded
- [ ] Manual testing completed

### Screenshots
- [ ] Real screenshots captured
- [ ] Stored in `docs/screenshots/`
- [ ] Embedded in DOCX

### Documentation
- [ ] Editable DOCX created
- [ ] Documentation matches implementation
- [ ] README completed
- [ ] Links included at the end

### Videos
- [ ] Real Demo Video created if recording is available
- [ ] Real Testing Video created if recording is available
- [ ] Both are 2–4 minutes
- [ ] Same male student voice used
- [ ] No fake footage/results

### Phases
- [ ] Phase 1 — Brainstorming & Ideation
- [ ] Phase 2 — Requirement Analysis
- [ ] Phase 3 — Project Design
- [ ] Phase 4 — Project Planning
- [ ] Phase 5 — Project Development
- [ ] Phase 6 — Project Testing
- [ ] Phase 7 — Project Documentation
- [ ] Phase 8 — Project Demonstration
- [ ] NO Phase 9

### GitHub
- [ ] Correct repository used
- [ ] Secrets excluded
- [ ] Clean commits
- [ ] Final changes pushed
- [ ] Repository URL verified

---

## 20. FINAL REPORT

At completion, provide:

### Project
- Project name
- Description
- Main technologies

### Execution
- Install command
- Run command
- Local URL if applicable

### Features
- Implemented core features

### Testing
- Test command
- Actual test result
- Manual validation result

### Screenshots
- Screenshot count
- Screenshot folder
- What they demonstrate

### Documentation
- DOCX path
- README path

### Videos
- Demo video path/link
- Testing video path/link
- Clearly state if recording was unavailable

### GitHub
- Repository URL
- Branch
- PR number if applicable
- Important commits

### Phase Structure

Confirm exactly:

1. Brainstorming & Ideation
2. Requirement Analysis
3. Project Design
4. Project Planning
5. Project Development
6. Project Testing
7. Project Documentation
8. Project Demonstration

Explicitly confirm:

**No Phase 9 was created.**

---

# FINAL RULE

Build a real project.

Use the **attached reference document** to decide **WHAT to build**.

Use **ComicCraft** only to understand **HOW a complete student project can be organized and documented**.

Do not clone ComicCraft.
Do not copy unrelated functionality.
Do not fabricate screenshots.
Do not fabricate tests.
Do not fabricate videos.
Do not invent features.
Do not claim success without actual verification.

The final result must be a genuine, runnable, testable, documented, and demonstrable academic project.
