# Development Roadmap & Phases

> **Status:** Active  
> **Last Updated:** July 24, 2026  
> **Version:** 1.0

---

## Table of Contents

- [1. Development Roadmap](#1-development-roadmap)
- [2. Current Phase](#2-current-phase)
- [3. Completed Phases](#3-completed-phases)
- [4. Upcoming Phases](#4-upcoming-phases)
- [5. Completion Criteria](#5-completion-criteria)
- [6. Progress Tracking](#6-progress-tracking)

---

## 1. Development Roadmap

### 1.1 Overview

CourseCraft-AI is being developed in a phased approach, starting with core backend services (mock AI), then frontend integration, real AI replacement, persistence, and finally production readiness. The README claims Phases 1–3 are complete, but the actual codebase shows significant gaps. This document reflects the **real** state of each phase based on code evidence.

### 1.2 Phase Summary

| Phase | Name | Status | Actual Completion |
|---|---|---|---|
| 1 | Core Backend (Mock AI) | 🔄 Partially Complete | ~65% |
| 2 | Frontend Integration | 🔄 Partially Complete | ~50% |
| 3 | Real AI + Persistence | ⬜ Not Started | 0% |
| 4 | Auth + User Management | ⬜ Not Started | 0% |
| 5 | Polish + Deployment | ⬜ Not Started | 0% |

---

## 2. Current Phase

### Phase 2: Frontend Integration

> **Status:** 🔄 In Progress  
> **Blocking Issues:** 3 critical frontend components are empty stubs

#### Objective

Connect the backend API to a complete frontend experience — users should be able to generate courses, view them, interact with mindmaps, study with flashcards, and ask questions.

#### Deliverables

| # | Deliverable | Status | Notes |
|---|---|---|---|
| 1 | Landing page | ✅ Complete | `index.jsx` — session input, navigation buttons, feature cards |
| 2 | Course detail page | ✅ Complete | `course/[id].jsx` — PDF, assignment, flashcard generation |
| 3 | Mindmap viewer page | ✅ Complete | `mindmap/[id].jsx` — ReactFlow + sidebar + flashcard modal |
| 4 | Course generation form | ❌ Missing | `CourseForm.jsx` is empty stub. `generate.jsx` shows "Coming soon…" |
| 5 | Course content viewer | ❌ Missing | `CourseViewer.jsx` is empty stub. No page displays course weeks/days |
| 6 | AI teacher chat interface | ❌ Missing | `ChatWithTeacher.jsx` is empty stub. `ask.jsx` shows "Coming soon…" |
| 7 | Assignment viewer component | ✅ Complete | Groups by type, expandable answers, color-coded headers |
| 8 | Flashcard viewer component | ✅ Complete | Flip animation, keyboard navigation, progress bar |
| 9 | ReactFlow mindmap system | ✅ Complete | Custom nodes, ELK layout, expand/collapse, sidebar |
| 10 | Shared navigation/layout | ❌ Missing | Each page has its own header. No consistent navigation. |

#### Blockers & Risks

| Issue | Impact | Mitigation |
|---|---|---|
| CourseForm.jsx is empty | Users cannot initiate course creation from the frontend | Must be implemented before Phase 2 can close |
| CourseViewer.jsx is empty | Users cannot see generated course content | Must be implemented before Phase 2 can close |
| Hardcoded `localhost:8000` in all fetch calls | Will break in any non-local deployment | Extract to environment variable or config file |

---

## 3. Completed Phases

### Phase 1: Core Backend (Mock AI) — ~65% Complete

> **Status:** 🔄 Mostly Complete (2 stub files remain)

#### What Was Delivered

**Fully implemented:**
- FastAPI application structure with CORS, static file serving, exception handling
- Pydantic models for courses, requests, and responses (`course_models.py`, `request_models.py`, `response_models.py`)
- Mock LLM course generator — deterministic course creation from topic/duration/difficulty/language (`llm_service.py`)
- PDF generation pipeline — Course JSON → Markdown → ReportLab → PDF (`pdf_service.py`)
- RAG pipeline architecture — text extraction, chunking, mock embeddings, cosine similarity, retrieval, mock answer generation (`rag_service.py`)
- Mindmap generation — Mermaid text from course structure with optional server-side rendering (`mindmap_service.py`)
- Assignment generation — mock MCQ/SHORT/LONG question generation (`assignment_service.py`)
- Flashcard generation — topic-aware template banks with difficulty filtering (`flashcard_service.py`)
- Session management — in-memory store with TTL, CRUD, background cleanup thread (`session_store.py`)
- Utility layer — text chunking, mock embeddings, file I/O, text cleaning, filename sanitization
- API endpoints — 16 active endpoints across 5 route files
- Test suite — 3 test files for course generation, PDF, and RAG
- Startup script (`run.sh`) and environment configuration

**Not delivered (stub files):**
- `auth_routes.py` — `# TODO: Implement later`
- `studyplan_routes.py` — `# TODO: Implement later`
- `studyplan_service.py` — `# TODO: Implement later`

#### Known Issues from Phase 1

- 383 lines of commented-out WeasyPrint code in `pdf_service.py`
- Duplicate service: both `mindmap_service.py` and `mermaid_service.py` handle Mermaid rendering
- Some services use bare `except:` without specific exception types
- Dockerfile is empty (`# TODO: Add Docker configuration`)

---

## 4. Upcoming Phases

### Phase 3: Real AI + Persistence

> **Status:** ⬜ Not Started

#### Planned Scope

- Replace `mock_llm_course_generator()` with real LLM API calls (OpenAI, Ollama, or equivalent)
- Replace `mock_llm_rag_answer()` with real LLM Q&A over retrieved context
- Replace mock embeddings (SHA256) with real embedding model (OpenAI embeddings or sentence-transformers)
- Set up PostgreSQL or SQLite database for persistent storage
- Migrate `SessionStore` from in-memory dict to database-backed persistence
- Set up vector database (Chroma, FAISS, or Pinecone) for RAG index storage
- Add streaming response support for chat/Q&A endpoints

#### Prerequisites

- Phase 2 must be complete (all frontend pages functional)
- LLM API key or local model (Ollama) must be available
- Database server must be set up

#### Open Questions

- Which LLM provider (OpenAI, Anthropic, local Ollama)?
- Which embedding model (OpenAI `text-embedding-3-small`, sentence-transformers, local)?
- Which database (PostgreSQL for relational data, SQLite for simplicity)?
- Which vector store (Chroma for local, Pinecone for cloud)?

---

### Phase 4: Auth + User Management

> **Status:** ⬜ Not Started

#### Planned Scope

- Implement JWT-based authentication (register, login, logout, refresh)
- Create User model and database table
- Complete `auth_routes.py` with full auth endpoints
- Add course ownership (user → courses relationship)
- Create login/signup frontend pages
- Add auth middleware to protected API routes
- Implement course history/listing page for logged-in users

#### Prerequisites

- Phase 3 must be complete (database must exist)

---

### Phase 5: Polish + Deployment

> **Status:** ⬜ Not Started

#### Planned Scope

- Implement Study Plan generator (complete stub routes + service)
- Complete Dockerfile for backend and frontend
- Create docker-compose for full-stack orchestration
- Set up CI/CD pipeline (GitHub Actions)
- Security hardening: restrict CORS, add rate limiting, enforce HTTPS
- Add shared navigation/layout component
- Mobile responsive optimization
- Accessibility improvements (ARIA labels, focus management, screen reader support)
- Error boundary components for frontend
- Fill all remaining documentation

#### Prerequisites

- Phases 3 and 4 must be complete

---

## 5. Completion Criteria

### 5.1 Definition of Done (Per Feature)

- [ ] Backend endpoint(s) implemented and returning correct responses
- [ ] Frontend UI connected to backend and rendering data
- [ ] Error states handled (loading, error, empty states)
- [ ] At least one test covers the happy path
- [ ] No hardcoded mock data in the feature path (unless explicitly mock mode)
- [ ] Code follows project rules (see `rules.md`)

### 5.2 Phase Sign-Off Criteria

- [ ] All deliverables in the phase are marked as complete
- [ ] No critical blockers remain
- [ ] All new endpoints are documented in the API endpoint map
- [ ] Tests pass: `pytest backend/tests/`
- [ ] Frontend builds without errors: `npm run build`
- [ ] Documentation updated to reflect new state

---

## 6. Progress Tracking

### 6.1 Overall Progress

| Metric | Value |
|---|---|
| Total Phases | 5 |
| Completed | 0 (Phase 1 is ~65%, Phase 2 is ~50%) |
| In Progress | 2 (Phases 1 and 2) |
| Remaining | 3 (Phases 3, 4, 5) |
| Overall Completion | ~35% |

### 6.2 Feature Completion by Area

| Area | Implemented | Total Planned | Completion |
|---|---|---|---|
| Backend Routes | 5 active / 7 total | 7 | 71% |
| Backend Services | 7 active / 8 total | 8 | 87% (but all mock AI) |
| Frontend Pages | 3 real / 5 total | 8+ planned | 37% |
| Frontend Components | 5 real / 8 total | 12+ planned | 42% |
| ReactFlow Mindmap System | 8 files | 8 files | 100% |
| Flashcard System | 6 files (4 FE + 2 BE) | 6 files | 100% |
| Database | 0 | 1 | 0% |
| Authentication | 0 | 1 | 0% |
| Real AI Integration | 0 | 3 (LLM, embeddings, RAG) | 0% |
| Deployment | 0 | 1 | 0% |
| Documentation | 0 filled / 10 templates | 10 | 0% → now being addressed |

### 6.3 Milestone Log

| Date | Milestone | Phase | Notes |
|---|---|---|---|
| — | Backend API scaffolding complete | 1 | FastAPI app with routes, services, models, utils |
| — | Mock course generation working | 1 | Deterministic course JSON from topic/difficulty |
| — | PDF generation pipeline working | 1 | ReportLab replaced WeasyPrint |
| — | RAG pipeline architecture implemented | 1 | Chunking → mock embeddings → cosine similarity → retrieval |
| — | Mindmap system complete | 2 | ReactFlow + ELK.js + custom nodes + expand/collapse |
| — | Flashcard system complete | 2 | Frontend viewers + modal + backend generation |
| — | Assignment viewer complete | 2 | Grouped by type, expandable answers |
| July 24, 2026 | Project audit completed | — | Full codebase analysis, identified gaps, documented state |
| July 24, 2026 | Documentation generated | — | PRD, architecture, design, rules, phases, project-state |

---

> _This document reflects the actual state of development based on code evidence as of July 24, 2026. Phase statuses are determined by what code exists, not by README claims._