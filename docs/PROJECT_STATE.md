# Project State

> **Last Updated:** July 24, 2026  
> **Current Phase:** Phase 2 — Frontend Integration  
> **Overall Status:** 🟡 At Risk — 3 critical frontend components are missing

---

## Table of Contents

- [1. Current Status](#1-current-status)
- [2. Features Completed](#2-features-completed)
- [3. Features In Progress](#3-features-in-progress)
- [4. Pending Work](#4-pending-work)
- [5. Known Issues](#5-known-issues)
- [6. Recent Decisions](#6-recent-decisions)
- [7. Next Steps](#7-next-steps)
- [8. Development Notes](#8-development-notes)

---

## 1. Current Status

### 1.1 Summary

CourseCraft-AI is an early-stage prototype at approximately 35% overall completion. The backend has a solid architectural foundation with clean separation of concerns, but all AI functionality is mock/template-based. The frontend has excellent mindmap visualization and flashcard components, but three critical pages (course generation form, course viewer, AI chat) are empty stubs. There is no database, no authentication, and no real LLM integration.

### 1.2 Health Dashboard

| Area | Status | Notes |
|---|---|---|
| Frontend | 🟡 Attention | 3 stub components, 2 placeholder pages, hardcoded API URLs |
| Backend | 🟢 Healthy | Well-structured; 16 active endpoints; all services functional (mock) |
| AI/LLM | 🔴 Critical | 100% mock — no real AI anywhere. Core value proposition not delivered. |
| Database | 🔴 Critical | No database. In-memory store only. All data lost on restart. |
| Deployment | 🔴 Critical | Empty Dockerfile. No CI/CD. Local-only. |
| Documentation | 🟡 Attention | Was entirely empty templates. Now being populated (this document). |

---

## 2. Features Completed

| # | Feature | Phase | Notes |
|---|---|---|---|
| 1 | FastAPI application scaffold | 1 | CORS, exception handling, router registration, static files |
| 2 | Pydantic data models | 1 | Course, request, and response schemas (3 files) |
| 3 | Mock course generation | 1 | Deterministic course JSON from topic/duration/difficulty/language |
| 4 | PDF generation (ReportLab) | 1 | Course JSON → Markdown → ReportLab → downloadable PDF |
| 5 | RAG pipeline architecture | 1 | Chunking, mock embeddings, cosine similarity, top-k retrieval |
| 6 | Mock Q&A answer generation | 1 | Keyword-based response selection over retrieved chunks |
| 7 | Mermaid mindmap generation | 1 | Styled Mermaid `graph TB` from course structure |
| 8 | Mock assignment generation | 1 | MCQ/SHORT/LONG question templates |
| 9 | Mock flashcard generation | 1 | Topic-aware flashcard banks with difficulty filtering |
| 10 | Session management | 1 | In-memory store with TTL, CRUD, background cleanup |
| 11 | Utility layer | 1 | Chunking, embeddings, file I/O, text cleaning, mermaid rendering |
| 12 | Landing page | 2 | Session input, navigation, feature cards |
| 13 | Course detail page | 2 | PDF/Assignment/Flashcard generation buttons and viewers |
| 14 | ReactFlow mindmap viewer | 2 | Custom nodes, ELK layout, expand/collapse, sidebar, minimap |
| 15 | Flashcard viewer component | 2 | Flip animation, keyboard nav, progress bar |
| 16 | Flashcard modal component | 2 | Modal overlay with loading skeleton, controls, regeneration |
| 17 | Assignment viewer component | 2 | Type-grouped questions, expandable answers, color coding |
| 18 | Test suite (3 files) | 1 | Course generator, PDF, RAG tests |
| 19 | Startup script | 1 | `run.sh` for venv, install, test, and uvicorn start |

---

## 3. Features In Progress

| # | Feature | Progress | Blockers | Notes |
|---|---|---|---|---|
| 1 | Course generation form (frontend) | 0% | No blocker — needs implementation | `CourseForm.jsx` is `// TODO`. `generate.jsx` is placeholder. |
| 2 | Course content viewer (frontend) | 0% | No blocker — needs implementation | `CourseViewer.jsx` is `// TODO`. No page displays course weeks/days. |
| 3 | AI teacher chat (frontend) | 0% | No blocker — needs implementation | `ChatWithTeacher.jsx` is `// TODO`. `ask.jsx` is placeholder. Backend `/api/v1/ask` exists but returns mock answers. |

---

## 4. Pending Work

### 4.1 High Priority

| # | Task | Phase | Dependencies | Notes |
|---|---|---|---|---|
| 1 | Implement CourseForm.jsx | 2 | None | Topic, duration, difficulty, language form → POST /api/v1/generate-course |
| 2 | Implement CourseViewer.jsx | 2 | None | Display weeks, days, objectives, content from session data |
| 3 | Implement ChatWithTeacher.jsx | 2 | None | Chat UI with message list → POST /api/v1/ask |
| 4 | Integrate real LLM | 3 | API key / Ollama setup | Replace mock_llm_course_generator and mock_llm_rag_answer |
| 5 | Add database | 3 | Database server | Replace in-memory SessionStore with PostgreSQL/SQLite |
| 6 | Replace mock embeddings | 3 | Embedding model | Replace SHA256 mock with real embedding model |
| 7 | Implement authentication | 4 | Database exists | Complete auth_routes.py, add JWT/OAuth |

### 4.2 Medium Priority

| # | Task | Phase | Dependencies | Notes |
|---|---|---|---|---|
| 8 | Add shared navigation component | 2 | None | Consistent header/nav across all pages |
| 9 | Implement study plan generator | 3+ | Real LLM | Complete studyplan_routes.py + studyplan_service.py |
| 10 | Add vector database for RAG | 3 | Database | Replace JSON file indices with Chroma/FAISS |
| 11 | Complete Dockerfile | 5 | None | Currently empty |
| 12 | Add docker-compose | 5 | Dockerfile | Full-stack orchestration |
| 13 | Extract API base URL to config | 2 | None | Remove hardcoded localhost:8000 from frontend |
| 14 | Add streaming chat responses | 3 | Real LLM | SSE or WebSocket for AI teacher chat |

### 4.3 Low Priority

| # | Task | Phase | Dependencies | Notes |
|---|---|---|---|---|
| 15 | Implement voice mode (TTS + STT) | 4+ | Real LLM | Claimed in README but zero code exists |
| 16 | Implement syllabus alignment | 4+ | PDF parsing | Claimed in README but zero code exists |
| 17 | Add analytics dashboard | 4+ | Auth + Database | Claimed in README but zero code exists |
| 18 | Multi-language content (real Hindi) | 3+ | Real LLM | Backend accepts "hindi" but content is always English |
| 19 | CI/CD pipeline | 5 | Docker | GitHub Actions or equivalent |
| 20 | Mobile responsive optimization | 5 | None | Basic responsive exists but not optimized |
| 21 | Accessibility improvements | 5 | None | No ARIA labels, limited keyboard nav |

---

## 5. Known Issues

| # | Issue | Severity | Area | Workaround | Status |
|---|---|---|---|---|---|
| 1 | All AI is mock — no real LLM integrated | 🔴 Critical | AI/LLM | Mock services produce deterministic template output | Open |
| 2 | No database — all data in-memory | 🔴 Critical | Backend | Data is lost on every server restart | Open |
| 3 | README claims features that don't exist | 🔴 Critical | Docs | 8+ features marked "✅ Complete" with zero code | Open |
| 4 | No authentication | 🔴 Critical | Security | All endpoints publicly accessible | Open |
| 5 | 383 lines of commented-out code in pdf_service.py | 🟡 Medium | Backend | Old WeasyPrint pipeline; active code works fine | Open |
| 6 | Duplicate services: mindmap_service.py vs mermaid_service.py | 🟡 Medium | Backend | Both handle Mermaid rendering with overlapping logic | Open |
| 7 | Hardcoded `http://localhost:8000` in frontend | 🟡 Medium | Frontend | Works in local dev only; will break in deployment | Open |
| 8 | CORS allows all origins (`*`) | 🟡 Medium | Security | Acceptable for development, must change for production | Open |
| 9 | Bare `except:` in some services | 🟢 Low | Backend | Catches all exceptions without specificity | Open |
| 10 | Some services use `print()` instead of `logger` | 🟢 Low | Backend | Inconsistent logging in mindmap_service.py | Open |
| 11 | Flashcard dot indicators are 12px (below 44px touch target) | 🟢 Low | Frontend | Usability issue on touch devices | Open |
| 12 | Mindmap route handler is synchronous (`def` not `async def`) | 🟢 Low | Backend | May block event loop under load | Open |
| 13 | Empty Dockerfile | 🟡 Medium | DevOps | Cannot containerize application | Open |

---

## 6. Recent Decisions

| Date | Decision | Rationale | Impact |
|---|---|---|---|
| Pre-audit | Switched PDF engine from WeasyPrint to ReportLab | WeasyPrint has system dependencies (Cairo, Pango) that are problematic on Windows | Old code commented out (383 lines) but not removed |
| Pre-audit | Adopted ReactFlow + ELK.js over client-side Mermaid rendering | Interactive mindmap with expand/collapse, zoom, sidebar provides far richer UX | Legacy Mermaid components still present but superseded |
| Pre-audit | Used mock/template AI instead of real LLM | Enables full stack development without LLM API costs; deterministic testing | Core product value not yet delivered |
| Pre-audit | In-memory session store instead of database | Fastest path to working prototype; zero infrastructure setup | Cannot persist data; cannot scale horizontally |
| July 24, 2026 | Conducted full project audit | Needed accurate understanding of what's built vs. what's claimed | 11-section audit report generated; all documentation gaps identified |
| July 24, 2026 | Generated production documentation from audit | All 10 doc templates were empty; project needed real documentation | 6 documents (PRD, architecture, design, rules, phases, project-state) created |

---

## 7. Next Steps

### Immediate (This Sprint)

- [ ] Implement `CourseForm.jsx` — topic input, duration slider, difficulty selector, language dropdown, submit button
- [ ] Implement `CourseViewer.jsx` — render course weeks/days/objectives/content in structured layout
- [ ] Connect `generate.jsx` page to backend via CourseForm → POST `/api/v1/generate-course`
- [ ] Extract `http://localhost:8000` to environment variable / config constant
- [ ] Add shared Layout/Navigation component with consistent header across pages

### Short Term (Next 2–4 Sprints)

- [ ] Implement `ChatWithTeacher.jsx` — chat message list, input box, send button → POST `/api/v1/ask`
- [ ] Connect `ask.jsx` page with ChatWithTeacher component
- [ ] Integrate real LLM (OpenAI API or local Ollama) for course generation
- [ ] Replace mock embeddings with real embedding model
- [ ] Set up database (PostgreSQL or SQLite) and migrate session storage
- [ ] Clean up 383 lines of dead WeasyPrint code in `pdf_service.py`
- [ ] Consolidate `mindmap_service.py` and `mermaid_service.py` into single service

### Medium Term (Next Quarter)

- [ ] Implement authentication (JWT)
- [ ] Complete `auth_routes.py` with register/login/logout endpoints
- [ ] Implement study plan generator (routes + service)
- [ ] Set up vector database for RAG indices
- [ ] Complete Dockerfile and docker-compose
- [ ] Fix README to accurately reflect feature completion status
- [ ] Add CI/CD pipeline

---

## 8. Development Notes

### 8.1 Environment Setup Notes

**Backend:**
1. Requires Python 3.8+
2. Run `run.sh` to auto-create venv, install deps, create directories, and start server
3. Alternatively: `pip install -r requirements.txt` then `uvicorn app.main:app --reload`
4. Server starts at `http://localhost:8000`
5. API docs at `http://localhost:8000/docs`

**Frontend:**
1. Requires Node.js 18+
2. `cd frontend && npm install && npm run dev`
3. Server starts at `http://localhost:3000`
4. Requires backend running on port 8000

**Environment Variables (`.env`):**
```
LLM_API_KEY=mock-key
EMBEDDING_MODEL=mock-embedding
SESSION_TTL=86400
```

### 8.2 Technical Debt

| # | Description | Impact | Priority | Effort |
|---|---|---|---|---|
| 1 | 383 lines of commented WeasyPrint code in pdf_service.py | Clutters primary service file; confuses new developers | Medium | Low (delete) |
| 2 | Duplicate mermaid services (mindmap_service.py + mermaid_service.py) | Unclear which to use; overlapping rendering logic | Medium | Medium (consolidate) |
| 3 | Hardcoded `http://localhost:8000` in 5+ frontend files | Blocks non-local deployment | High | Low (extract to config) |
| 4 | Bare `except:` clauses in rag_service.py and other services | Swallows unexpected errors; hides bugs | Low | Low (add exception types) |
| 5 | `print()` used instead of `logger` in mindmap_service.py | Inconsistent logging; no log level control | Low | Low (replace) |
| 6 | Empty Dockerfile | Cannot containerize; blocks deployment | Medium | Medium (implement) |
| 7 | README falsely claims 8+ features as complete | Misleads contributors and stakeholders | High | Low (update) |
| 8 | Legacy Mermaid components (MindmapViewer, ZoomableMermaidRenderer) | Superseded by ReactFlow system; dead code | Low | Low (remove or document as legacy) |

### 8.3 Session Log

| Date | What Was Done | What's Next |
|---|---|---|
| July 24, 2026 | Complete project audit performed — every file in repository examined | Generate production documentation |
| July 24, 2026 | 6 documentation files generated from audit findings (PRD, architecture, design, rules, phases, project-state) | Implement missing frontend components (CourseForm, CourseViewer, ChatWithTeacher) |

---

> _Update this document at the start and end of each development session. It is the living snapshot of the project._