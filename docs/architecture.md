# Architecture Document

> **Status:** Active  
> **Last Updated:** July 24, 2026  
> **Version:** 1.0

---

## Table of Contents

- [1. System Architecture](#1-system-architecture)
- [2. Frontend Architecture](#2-frontend-architecture)
- [3. Backend Architecture](#3-backend-architecture)
- [4. Folder Structure](#4-folder-structure)
- [5. API Architecture](#5-api-architecture)
- [6. Data Flow](#6-data-flow)
- [7. Tech Stack](#7-tech-stack)
- [8. Deployment](#8-deployment)
- [9. Scalability](#9-scalability)

---

## 1. System Architecture

### 1.1 Overview

CourseCraft-AI is a client-server application with a decoupled frontend and backend communicating over REST APIs. The frontend is a Next.js 14 application that makes HTTP requests to a FastAPI backend. There is no database—all state is held in an in-memory session store with TTL-based expiration.

AI functionality is currently implemented via mock/template-based services designed to be swapped with real LLM integrations without architectural changes.

### 1.2 Architecture Diagram

```
┌──────────────────────────────┐         ┌────────────────────────────────────────────┐
│       Frontend (Next.js)     │         │          Backend (FastAPI)                 │
│       localhost:3000         │         │          localhost:8000                    │
│                              │  HTTP   │                                            │
│  Pages:                      │────────▶│  Routes (API Layer)                        │
│  ├─ index.jsx (Landing)      │         │  ├─ course_routes.py     (5 endpoints)     │
│  ├─ course/[id].jsx          │         │  ├─ rag_routes.py        (4 endpoints)     │
│  ├─ mindmap/[id].jsx         │         │  ├─ mindmap_routes.py    (1 endpoint)      │
│  ├─ generate.jsx (stub)      │         │  ├─ assignment_routes.py (2 endpoints)     │
│  └─ ask.jsx (stub)           │         │  ├─ flashcard_routes.py  (2 endpoints)     │
│                              │         │  ├─ auth_routes.py       (empty)           │
│  Components:                 │         │  └─ studyplan_routes.py  (empty)           │
│  ├─ reactflow/ (mindmap)     │         │                                            │
│  ├─ flashcards/ (cards)      │         │  Services (Business Logic)                 │
│  ├─ AssignmentViewer.jsx     │         │  ├─ llm_service.py       (mock AI)         │
│  ├─ FlashcardViewer.jsx      │         │  ├─ rag_service.py       (RAG pipeline)    │
│  ├─ CourseForm.jsx (stub)    │         │  ├─ pdf_service.py       (ReportLab)       │
│  ├─ CourseViewer.jsx (stub)  │         │  ├─ mindmap_service.py   (Mermaid gen)     │
│  └─ ChatWithTeacher (stub)   │         │  ├─ mermaid_service.py   (HD rendering)    │
│                              │         │  ├─ assignment_service.py (mock gen)       │
│                              │         │  ├─ flashcard_service.py  (template gen)   │
│                              │         │  └─ studyplan_service.py  (empty)          │
│                              │         │                                            │
│                              │         │  Utils (Shared)                             │
│                              │         │  ├─ session_store.py     (in-memory)       │
│                              │         │  ├─ chunking.py          (text splitter)   │
│                              │         │  ├─ embeddings.py        (mock 128-dim)    │
│                              │         │  ├─ file_manager.py      (file I/O)        │
│                              │         │  ├─ text_cleaner.py      (text utils)      │
│                              │         │  └─ mermaid_renderer.py  (diagram gen)     │
│                              │         │                                            │
│                              │         │  Models (Pydantic)                          │
│                              │         │  ├─ course_models.py                       │
│                              │         │  ├─ request_models.py                      │
│                              │         │  └─ response_models.py                     │
│                              │         │                                            │
│                              │◀────────│  Static Files                               │
│                              │  Files  │  ├─ /static/pdf/         (generated PDFs)  │
│                              │         │  └─ /static/mindmaps/    (generated maps)  │
└──────────────────────────────┘         └────────────────────────────────────────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  In-Memory Store │
                                                 │  (Python dict    │
                                                 │   + threading)   │
                                                 │                  │
                                                 │  No Database     │
                                                 │  No Vector DB    │
                                                 │  No External API │
                                                 └─────────────────┘
```

### 1.3 Key Design Decisions

| Decision | Rationale | Trade-offs |
|---|---|---|
| Mock-first AI services | Enables full stack development without LLM costs; deterministic testing | No real intelligence; content is template-based |
| In-memory session store | Fastest path to working prototype; no DB setup required | Data lost on restart; cannot scale horizontally |
| ReportLab for PDF (not WeasyPrint) | Windows-compatible; pure Python; no system dependencies | Less CSS control than WeasyPrint; simpler output styling |
| ReactFlow for mindmap (not Mermaid client render) | Interactive zoom/pan/expand; richer UX than static SVG | More complex component code; larger bundle |
| ELK.js for auto-layout | Produces clean hierarchical layouts automatically | Async layout computation; adds JS bundle size |
| Decoupled frontend/backend | Independent deployment; clear API contract; team parallelism | CORS required; two processes to run locally |
| Session-based architecture | Stateless backend per request; sessions link course lifecycle | Sessions are ephemeral; no user-course persistence |

---

## 2. Frontend Architecture

### 2.1 Framework & Rendering Strategy

- **Framework:** Next.js 14 (Pages Router)
- **Rendering:** Client-side rendering (CSR) for all pages. No SSR/SSG used.
- **Routing:** File-based routing via `pages/` directory. Dynamic routes for `course/[id]` and `mindmap/[id]`.
- **Styling:** TailwindCSS 3 with custom theme extensions.

### 2.2 State Management

- **Approach:** Local component state via React `useState` and `useEffect` hooks
- **No global state:** No Redux, Zustand, or Context API
- **Data fetching:** Direct `fetch()` calls to backend API within components
- **Session ID:** Passed via URL query parameters and dynamic route segments

### 2.3 Component Architecture

```
App (_app.jsx)
├── Pages
│   ├── index.jsx .................. Landing page (session input, navigation)
│   ├── course/[id].jsx ........... PDF/Assignment/Flashcard generation
│   ├── mindmap/[id].jsx .......... Interactive mindmap viewer
│   ├── generate.jsx .............. STUB — "Coming soon…"
│   └── ask.jsx ................... STUB — "Coming soon…"
│
├── Implemented Components
│   ├── AssignmentViewer.jsx ....... Groups by type, expandable answers
│   ├── FlashcardViewer.jsx ........ Flip card with keyboard navigation
│   ├── MindmapViewer.jsx .......... Legacy Mermaid-based viewer
│   ├── MermaidRenderer.jsx ........ Mermaid client render
│   ├── ZoomableMermaidRenderer.jsx. Zoom/pan wrapper
│   │
│   ├── reactflow/
│   │   ├── MindmapFlow.jsx ........ Core ReactFlow + ELK layout
│   │   ├── Sidebar.jsx ............ Node detail panel
│   │   ├── nodes/
│   │   │   ├── CourseNode.jsx
│   │   │   ├── WeekNode.jsx
│   │   │   └── DayNode.jsx
│   │   ├── edges/
│   │   │   └── CustomEdge.jsx
│   │   └── utils/
│   │       ├── convertMermaidToGraph.js
│   │       └── elkLayout.js
│   │
│   └── flashcards/
│       ├── Flashcard.jsx
│       ├── FlashcardControls.jsx
│       ├── FlashcardModal.jsx
│       └── FlashcardSkeleton.jsx
│
└── Stub Components (empty — "TODO: Implement component")
    ├── CourseForm.jsx
    ├── CourseViewer.jsx
    └── ChatWithTeacher.jsx
```

### 2.4 Styling Strategy

- **CSS Framework:** TailwindCSS 3 with PostCSS + Autoprefixer
- **Custom Theme:** Extended Tailwind config with project-specific color palettes (course/week/day/canvas), custom animations (fade-in, slide-in-right, pulse-soft, glow), node shadow variants, and Inter/JetBrains Mono font families
- **Global CSS:** `styles/globals.css` (8KB) with base resets and ReactFlow overrides
- **Responsive:** Basic responsive utilities (`sm:`, `md:` breakpoints). Desktop-first. Not optimized for mobile.

---

## 3. Backend Architecture

### 3.1 Framework & Patterns

- **Framework:** FastAPI 0.104.1 with Uvicorn ASGI server
- **Pattern:** Layered architecture — Routes → Services → Utils/Models
- **Validation:** Pydantic v2 models for all request/response schemas
- **Async:** Route handlers are `async def` (except mindmap which is synchronous `def`)

### 3.2 Module Structure

| Module | Responsibility |
|---|---|
| `routes/` | HTTP endpoint handlers, request validation, response formatting |
| `services/` | Business logic, AI pipelines, content generation, PDF creation |
| `models/` | Pydantic data models for courses, requests, and responses |
| `utils/` | Shared utilities: session storage, chunking, embeddings, file I/O, text processing |
| `templates/` | Markdown templates for course, assignment, flashcard rendering |
| `static/` | Output directories for generated PDFs and mindmap images |

### 3.3 Middleware & Plugins

| Middleware | Purpose |
|---|---|
| CORSMiddleware | Cross-origin requests; currently allows all origins (`*`) |
| StaticFiles (PDF) | Serves generated PDFs at `/static/pdf/` |
| StaticFiles (Mindmaps) | Serves generated mindmap images at `/static/mindmaps/` |
| Custom Exception Handler (HTTP) | Returns structured `{error, message, success}` JSON for HTTP exceptions |
| Custom Exception Handler (General) | Catches unhandled exceptions, logs them, returns 500 |

### 3.4 Authentication & Authorization

**Not implemented.** The `auth_routes.py` file contains only `# TODO: Implement later` and is commented out in `main.py`. All endpoints are publicly accessible without authentication.

### 3.5 Error Handling Strategy

- Every route handler wraps logic in `try/except`
- `HTTPException` is re-raised for known errors (400, 404)
- General `Exception` is caught and wrapped in 500 response
- Custom exception handlers in `main.py` ensure consistent JSON error format
- Logging via Python `logging` module at ERROR level for all caught exceptions
- **Known issue:** Some services use bare `except:` without specific exception types (e.g., `rag_service.py` line 76)

---

## 4. Folder Structure

### 4.1 Root Structure

```
CourseCraft-AI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py ............... FastAPI app, middleware, router registration
│   │   ├── config.py ............. Environment variables, constants
│   │   ├── models/ ............... Pydantic schemas (3 files)
│   │   ├── routes/ ............... API endpoints (7 files, 2 empty)
│   │   ├── services/ ............. Business logic (8 files, 1 empty)
│   │   ├── utils/ ................ Shared utilities (6 files)
│   │   ├── templates/ ............ Markdown render templates (3 files)
│   │   └── static/ ............... Generated output (pdf/, mindmaps/)
│   ├── tests/ .................... Test suite (3 files)
│   ├── static/mindmaps/ .......... Mindmap output (also mounted)
│   ├── requirements.txt .......... Python dependencies (12 packages)
│   ├── Dockerfile ................ EMPTY — "# TODO: Add Docker configuration"
│   ├── run.sh .................... Bash startup script
│   ├── .env.example .............. Environment variable template
│   └── venv/ ..................... Python virtual environment
│
├── frontend/
│   ├── pages/ .................... Next.js pages (4 real + 2 stubs)
│   ├── components/ ............... React components (5 real + 3 stubs)
│   ├── styles/globals.css ........ Global CSS (8KB)
│   ├── package.json .............. Node dependencies (14 packages)
│   ├── tailwind.config.js ........ Custom Tailwind theme
│   ├── next.config.js ............ Webpack fallbacks for Mermaid
│   ├── postcss.config.js ......... PostCSS configuration
│   └── node_modules/ ............. Node modules
│
├── docs/ ......................... Project documentation
├── .env .......................... Root environment file (3 variables)
├── LICENSE ....................... License placeholder (20 bytes)
└── README.md ..................... Project README
```

### 4.2 Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Python files | snake_case | `course_routes.py`, `llm_service.py` |
| Python classes | PascalCase | `SessionStore`, `RAGService`, `GenerateCourseRequest` |
| Python functions | snake_case | `generate_course_pdf()`, `mock_llm_course_generator()` |
| React components | PascalCase files + export | `MindmapFlow.jsx`, `FlashcardViewer.jsx` |
| React pages | lowercase or `[param]` | `index.jsx`, `[id].jsx` |
| CSS classes | Tailwind utility classes | `bg-gradient-to-br from-blue-600` |
| API endpoints | kebab-case | `/generate-course`, `/generate-pdf` |
| Session IDs | `session_` prefix + UUID | `session_a1b2c3d4e5f6...` |

---

## 5. API Architecture

### 5.1 Design Principles

- RESTful endpoints with JSON request/response bodies
- API versioning via URL prefix (`/api/v1/`)
- Consistent error response format across all endpoints
- Pydantic model validation on all request bodies
- Auto-generated OpenAPI/Swagger documentation at `/docs`

### 5.2 Base URL & Versioning

| Environment | Base URL |
|---|---|
| Development | `http://localhost:8000/api/v1` |
| Production | Not configured |

### 5.3 Endpoint Map

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/` | Root welcome message | No |
| `GET` | `/health` | Health check | No |
| `GET` | `/api/v1/status` | API feature status | No |
| `POST` | `/api/v1/generate-course` | Generate course JSON | No |
| `POST` | `/api/v1/generate-pdf` | Generate course PDF | No |
| `GET` | `/api/v1/course/{session_id}` | Get course data | No |
| `GET` | `/api/v1/session/{session_id}` | Get session info | No |
| `GET` | `/api/v1/sessions` | List all sessions (debug) | No |
| `DELETE` | `/api/v1/session/{session_id}` | Delete session | No |
| `POST` | `/api/v1/ask` | RAG Q&A | No |
| `GET` | `/api/v1/rag-info/{session_id}` | RAG system info (debug) | No |
| `POST` | `/api/v1/rag-simulate/{session_id}` | Simulate RAG query (debug) | No |
| `GET` | `/api/v1/rag-chunks/{session_id}` | Get chunk details (debug) | No |
| `POST` | `/api/v1/mindmap/generate` | Generate mindmap | No |
| `POST` | `/api/v1/assignments/generate` | Generate assignments | No |
| `GET` | `/api/v1/assignments/{session_id}` | Get assignments | No |
| `POST` | `/api/v1/flashcards/generate` | Generate flashcards | No |
| `GET` | `/api/v1/flashcards/{session_id}` | Get flashcards | No |

**Total: 18 active endpoints, 2 empty stub route files (auth, studyplan)**

### 5.4 Request/Response Format

**Standard Success Response:**
```json
{
  "success": true,
  "session_id": "session_abc123...",
  "message": "Course generated successfully",
  "data": { }
}
```

**Standard Error Response:**
```json
{
  "error": true,
  "message": "Session not found or expired",
  "success": false
}
```

### 5.5 Status Codes

| Code | Usage |
|---|---|
| `200` | Successful request |
| `400` | Bad request / validation error (invalid duration, difficulty, language) |
| `404` | Session not found or expired; no course data in session |
| `500` | Internal server error (generation failure, unhandled exceptions) |

---

## 6. Data Flow

### 6.1 Request Lifecycle

```
Client (Browser)
  → HTTP Request
    → FastAPI Router
      → Route Handler (validation, session lookup)
        → Service Layer (business logic, AI pipeline)
          → Utils (session store, chunking, embeddings, file I/O)
        ← Returns result
      ← Formats response (Pydantic model)
    ← JSON Response
  ← Rendered in React component
```

### 6.2 Key Data Flows

#### Flow: Course Generation

```
POST /api/v1/generate-course
  { topic, duration, difficulty, language }
    → course_routes.py: validate inputs
      → llm_service.py: mock_llm_course_generator()
        → Generates deterministic course structure using MD5 seed
        → Creates Week/Day/Assignment/Flashcard Pydantic models
      ← Returns course_data dict
    → session_store: create_session(course_data)
    ← Returns { session_id, course, success }
```

#### Flow: PDF Generation

```
POST /api/v1/generate-pdf
  { session_id }
    → course_routes.py: lookup session
      → session_store.get_session()
    → pdf_service.py: generate_course_pdf()
      → course_to_markdown(): Course JSON → Markdown string
      → parse_markdown_to_story(): Markdown → ReportLab flowables
      → SimpleDocTemplate.build(): Flowables → PDF file
    ← Returns { pdf_url, success }
```

#### Flow: RAG Q&A

```
POST /api/v1/ask
  { session_id, query }
    → rag_routes.py: lookup session, get course data
    → rag_service.py:
      → If no index: create_rag_index()
        → Extract text via get_total_content()
        → chunk_course_content() → text chunks
        → get_text_embedding() for each chunk → mock 128-dim vectors
        → Save index to temp/rag_index_{id}.json
      → query_rag_index()
        → get_text_embedding(question)
        → cosine_similarity() for each chunk
        → Sort, get top-3 chunks
        → mock_llm_rag_answer(query, context, title) → keyword-based response
    ← Returns { answer, sources, success }
```

#### Flow: Mindmap Generation

```
POST /api/v1/mindmap/generate
  { session_id }
    → mindmap_routes.py: lookup session
    → mindmap_service.py:
      → generate_mermaid_text(course)
        → Builds Mermaid "graph TB" with styled nodes
      → save_mermaid_file() → .mmd file
      → render_mermaid_images()
        → Attempts npx @mermaid-js/mermaid-cli for PNG + SVG
        → Falls back to create_placeholder_svg() if CLI unavailable
    ← Returns { mermaid_text, png_url, svg_url, success }

Frontend receives mermaid_text:
  → convertMermaidToGraph.js: Parse → nodes[] + edges[]
  → elkLayout.js: Compute positions via ELK
  → MindmapFlow.jsx: Render in ReactFlow canvas
```

---

## 7. Tech Stack

### 7.1 Overview

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Frontend Framework | Next.js | 14.0.0 | React-based page routing and rendering |
| UI Library | React | 18.2.0 | Component-based UI |
| CSS | TailwindCSS | 3.4.19 | Utility-first styling |
| Mindmap Visualization | ReactFlow | 11.11.4 | Interactive node graph rendering |
| Graph Layout | ELK.js | 0.11.1 | Automatic hierarchical layout computation |
| Graph Layout (secondary) | Dagre | 0.8.5 | Alternative layout engine (available) |
| Diagram Rendering | Mermaid | 11.12.1 | Diagram syntax parsing (client-side) |
| Zoom/Pan | react-zoom-pan-pinch | 3.7.0 | Legacy Mermaid viewer zoom |
| Backend Framework | FastAPI | 0.104.1 | Async REST API |
| ASGI Server | Uvicorn | 0.24.0 | Production server |
| Data Validation | Pydantic | 2.5.0 | Request/response schemas |
| PDF Generation | ReportLab | latest | Markdown → PDF conversion |
| Markdown Processing | markdown | 3.6 | Markdown → HTML (currently unused after ReportLab switch) |
| Template Engine | Jinja2 | 3.1.2 | Markdown template rendering |
| File Uploads | python-multipart | 0.0.6 | Multipart form data support |
| Environment | python-dotenv | 1.0.0 | .env file loading |
| Testing | pytest | 7.4.3 | Test framework |
| Testing (async) | pytest-asyncio | 0.21.1 | Async test support |
| Production Server | gunicorn | 21.2.0 | WSGI/ASGI production server |

### 7.2 Key Dependencies

#### Frontend (`package.json`)

| Package | Purpose |
|---|---|
| `next` | Framework |
| `react` / `react-dom` | UI library |
| `tailwindcss` / `postcss` / `autoprefixer` | CSS toolchain |
| `reactflow` | Mindmap interactive canvas |
| `elkjs` | Automatic graph layout |
| `dagre` | Alternative layout engine |
| `mermaid` | Diagram rendering |
| `react-zoom-pan-pinch` | Legacy zoom/pan for Mermaid views |
| `@react-pdf-viewer/core` | PDF viewer (available, usage unclear) |
| `@reactflow/node-resizer` | ReactFlow node resizing extension |

#### Backend (`requirements.txt`)

| Package | Purpose |
|---|---|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `pydantic` | Data validation |
| `reportlab` | PDF generation |
| `markdown` | Markdown processing |
| `jinja2` | Template engine |
| `python-multipart` | File upload support |
| `python-dotenv` | Environment loading |
| `pytest` / `pytest-asyncio` | Testing |
| `gunicorn` | Production deployment |
| `weasyprint` | Listed in requirements but code is commented out |

---

## 8. Deployment

### 8.1 Environments

| Environment | Purpose | URL |
|---|---|---|
| Development | Local development | Backend: `http://localhost:8000`, Frontend: `http://localhost:3000` |
| Staging | Not configured | — |
| Production | Not configured | — |

### 8.2 Current Deployment Setup

- **Backend startup:** `run.sh` script handles venv creation, pip install, directory creation, `.env` loading, pytest, and `uvicorn` start
- **Frontend startup:** `npm run dev` (standard Next.js dev server)
- **Docker:** Dockerfile exists but is empty (`# TODO: Add Docker configuration`)
- **CI/CD:** None configured
- **No docker-compose** for full-stack orchestration

### 8.3 Environment Variables

| Variable | Description | Required | Default |
|---|---|---|---|
| `LLM_API_KEY` | API key for LLM service | No (mock mode) | `mock-key` |
| `EMBEDDING_MODEL` | Embedding model identifier | No (mock mode) | `mock-embedding` |
| `SESSION_TTL` | Session time-to-live in seconds | No | `86400` (24 hours) |

### 8.4 Infrastructure

Currently local-only. No cloud hosting, CDN, reverse proxy, or container orchestration configured.

---

## 9. Scalability

### 9.1 Current Capacity

- **Single process:** Uvicorn with `--reload` (development mode)
- **In-memory storage:** Limited by server RAM; all data lost on restart
- **No horizontal scaling:** Session store is process-local Python dict
- **No caching:** Every request regenerates content
- **Synchronous AI:** Mock AI is instant, but real LLM calls will block the event loop without async handling

### 9.2 Scaling Strategy (When Needed)

| Concern | Recommended Strategy |
|---|---|
| Horizontal Scaling | Replace in-memory SessionStore with Redis or PostgreSQL |
| Caching | Add Redis cache for generated courses and RAG indices |
| Rate Limiting | Add FastAPI rate limiting middleware |
| Load Balancing | Deploy behind Nginx or cloud load balancer |
| Async AI | Use background tasks (Celery/FastAPI BackgroundTasks) for LLM calls |
| Vector Store | Replace JSON file RAG index with Chroma, FAISS, or Pinecone |
| Static Assets | Serve PDFs and mindmap images via CDN |

### 9.3 Performance Targets (Not Yet Measured)

| Metric | Target |
|---|---|
| API Response Time (p95) | < 2 seconds (mock), < 30 seconds (real AI) |
| Page Load Time | < 3 seconds |
| Concurrent Users | Currently: 1 (single process, in-memory). Target: 100+ |
| Mindmap Render Time | < 5 seconds for courses up to 24 weeks |

---

> _This document describes the architecture as it exists today. No aspirational features are included unless explicitly marked as missing._
