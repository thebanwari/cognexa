# Project Rules

> **Status:** Active  
> **Last Updated:** July 24, 2026  
> **Version:** 1.0

---

## Table of Contents

- [1. Architecture Rules](#1-architecture-rules)
- [2. Backend Rules](#2-backend-rules)
- [3. Frontend Rules](#3-frontend-rules)
- [4. API Rules](#4-api-rules)
- [5. AI/LLM Rules](#5-aillm-rules)
- [6. Code Quality Rules](#6-code-quality-rules)
- [7. Security Rules](#7-security-rules)
- [8. Documentation Rules](#8-documentation-rules)
- [9. File & Naming Rules](#9-file--naming-rules)
- [10. Git & Workflow Rules](#10-git--workflow-rules)

---

## 1. Architecture Rules

### 1.1 Separation of Concerns

| Layer | Responsibility | What It Must NOT Do |
|---|---|---|
| `routes/` | HTTP handling, request validation, response formatting | Must not contain business logic, direct file I/O, or AI calls |
| `services/` | Business logic, AI pipelines, content generation | Must not import FastAPI types or handle HTTP concerns |
| `models/` | Data schemas and validation via Pydantic | Must not contain logic, I/O, or side effects |
| `utils/` | Shared pure utilities (chunking, embeddings, file I/O) | Must not import from routes or services |
| `templates/` | Markdown rendering templates | Must not contain Python logic |

### 1.2 Dependency Direction

```
routes → services → utils
routes → models
services → models
services → utils
```

- **Never** import routes from services, utils, or models.
- **Never** import services from utils.
- Models may be imported by any layer.

### 1.3 State Management

- All runtime state lives in the `SessionStore` (in-memory dict with TTL)
- No global mutable state outside of `session_store` and `rag_services` registry
- Session IDs are the primary key for all data lookups
- Generated files (PDFs, mindmaps) are stored in `static/` directories and served via FastAPI StaticFiles

### 1.4 Configuration

- All configurable values must be defined in `config.py`
- Values must be loaded from environment variables via `python-dotenv`
- Hardcoded magic numbers in services must reference `config.py` constants
- No secrets in source code; use `.env` file (excluded from git via `.gitignore`)

---

## 2. Backend Rules

### 2.1 Route Handlers

- Every route handler must be wrapped in `try/except`
- Known errors must raise `HTTPException` with appropriate status code (400, 404)
- Unknown errors must log the exception and return 500 with a generic message
- All request bodies must be validated using Pydantic models from `request_models.py`
- All responses must use Pydantic models from `response_models.py`

### 2.2 Service Layer

- Each feature area has its own service file (`llm_service.py`, `rag_service.py`, etc.)
- Services must be stateless functions or class instances (no request-scoped state)
- Mock implementations must be clearly marked with `mock_` prefix in function names
- When replacing mocks with real implementations, the function signature must remain identical

### 2.3 Models

- All course data structures are defined in `course_models.py`
- All API request schemas are defined in `request_models.py`
- All API response schemas are defined in `response_models.py`
- Model fields must have type annotations and descriptive field names
- Optional fields must have default values

### 2.4 Logging

- Use Python `logging` module, not `print()` statements
- Each module must create its own logger: `logger = logging.getLogger(__name__)`
- Log at `INFO` for normal operations, `WARNING` for recoverable issues, `ERROR` for failures
- Include context (session_id, file paths) in log messages

### 2.5 Testing

- Tests reside in `backend/tests/`
- Test files follow `test_<module>.py` naming convention
- Tests use `pytest` framework
- All mock service functions must have corresponding test coverage
- Tests must not depend on external services or network access

---

## 3. Frontend Rules

### 3.1 Pages

- Pages live in `frontend/pages/` using Next.js Pages Router file-based routing
- Each page is a default-exported React function component
- Dynamic routes use `[param].jsx` syntax (e.g., `[id].jsx`)
- Pages must include `<Head>` with `<title>` and `<meta description>` for SEO

### 3.2 Components

- Reusable components live in `frontend/components/`
- Feature-specific component groups have subdirectories (e.g., `reactflow/`, `flashcards/`)
- Components must be default-exported PascalCase functions
- Stub components must contain a `// TODO: Implement component` comment

### 3.3 State Management

- Use React `useState` and `useEffect` hooks for local state
- No global state management library is currently used
- Data fetching uses browser `fetch()` directly within components
- Session IDs are obtained from URL parameters via `useRouter`

### 3.4 Styling

- Use TailwindCSS utility classes exclusively for styling
- Custom theme values are defined in `tailwind.config.js`
- No inline `style={}` objects except for dynamic values (e.g., CSS custom properties, calculated widths)
- Global styles and overrides go in `styles/globals.css`
- Component-specific CSS custom properties (e.g., `--day-index`) are acceptable for animation

### 3.5 API Calls

- All backend calls target `http://localhost:8000` (hardcoded; needs environment variable)
- Use `async/await` with `fetch()` for API calls
- Always check `response.ok` before parsing JSON
- Handle errors in `catch` blocks and display user-facing error messages

---

## 4. API Rules

### 4.1 URL Design

- All API endpoints are prefixed with `/api/v1/`
- Endpoint names use kebab-case (e.g., `/generate-course`, `/generate-pdf`)
- Resource identifiers use path parameters (e.g., `/course/{session_id}`)
- No query parameters for data that should be in the request body

### 4.2 HTTP Methods

| Method | Usage |
|---|---|
| `GET` | Read operations (fetch course, session info, health check) |
| `POST` | Create/generate operations (generate course, PDF, mindmap, assignments) |
| `DELETE` | Delete operations (delete session) |

### 4.3 Response Format

All responses must follow this structure:

```json
{
  "success": true | false,
  "message": "Human-readable message",
  "session_id": "session_xxx (when applicable)",
  "data_field": { ... }
}
```

Error responses additionally include:
```json
{
  "error": true,
  "success": false,
  "message": "Error description"
}
```

### 4.4 Status Codes

| Code | When to Use |
|---|---|
| 200 | Successful request |
| 400 | Invalid input (bad duration, unknown difficulty, missing fields) |
| 404 | Session not found, course not found in session, resource missing |
| 500 | Unhandled server error, generation failure |

---

## 5. AI/LLM Rules

### 5.1 Current State (Mock Mode)

- All LLM functions are prefixed with `mock_` (e.g., `mock_llm_course_generator`, `mock_llm_rag_answer`)
- Mock functions must be deterministic — same inputs must produce same outputs
- Determinism is achieved via MD5/SHA256 hash seeding
- Mock functions must match the exact signature that real LLM functions will use

### 5.2 RAG Pipeline Rules

- Course text is extracted via the `Course.get_total_content()` method
- Text is chunked using sentence-boundary-aware splitting (700 char default, 100 char overlap)
- Embeddings are 128-dimensional vectors (mock: SHA256-based; real: must be same dimensionality)
- RAG indices are stored per-session and keyed by `session_id`
- Similarity search returns top-3 most relevant chunks by default
- RAG indices are persisted to `temp/rag_index_{session_id}.json`

### 5.3 Replacement Rules

When integrating a real LLM:
- Replace function bodies, not signatures, in `llm_service.py`
- Remove the `mock_` prefix from function names and update all callers
- Ensure real LLM calls are `async` to avoid blocking the event loop
- Add timeout handling and retry logic for API calls
- Update `config.py` with real API key and model configuration variables

---

## 6. Code Quality Rules

### 6.1 Python (Backend)

- Follow PEP 8 style guidelines
- All functions must have docstrings describing purpose, args, and return values
- Type annotations required on all function parameters and return types
- Maximum function length: aim for < 50 lines (currently violated by some services)
- No bare `except:` — always catch specific exception types
- Remove commented-out code before merging (currently violated: 383 lines in `pdf_service.py`)

### 6.2 JavaScript/JSX (Frontend)

- Use functional components with hooks (no class components)
- Destructure props in function parameters
- Use `const` by default; `let` only when reassignment is needed; never `var`
- Event handler functions use `handle` prefix (e.g., `handleFlip`, `handleNext`)
- Callback props use `on` prefix (e.g., `onNodeClick`, `onClose`)
- Effect dependencies must be explicitly listed (ESLint disable comments are acceptable with justification)

### 6.3 General

- No duplicate functionality across files (currently violated: `mindmap_service.py` vs `mermaid_service.py`)
- No hardcoded API URLs in frontend (currently violated: `http://localhost:8000` is hardcoded in multiple components)
- Every feature must have at least one corresponding test

---

## 7. Security Rules

### 7.1 Current State (Development Only)

| Concern | Current Implementation | Status |
|---|---|---|
| CORS | Allows all origins (`*`) | ⚠️ Must be restricted before production |
| Authentication | None | ❌ Missing |
| Rate Limiting | None | ❌ Missing |
| Input Validation | Pydantic models on request bodies | ✅ Adequate for current scope |
| Secrets | Stored in `.env` file | ✅ Adequate |
| HTTPS | Not enforced | ❌ Must be added for production |
| File Path Validation | `sanitize_filename()` exists in utils | ✅ Present |

### 7.2 Rules for Production

- CORS origins must be restricted to specific frontend domain(s)
- All mutating endpoints must require authentication
- Rate limiting must be applied (recommended: 60 requests/minute per IP)
- API keys must never be committed to version control
- User-supplied text must be sanitized before use in file paths or shell commands
- Static file serving must be restricted to expected file types (PDF, PNG, SVG)

---

## 8. Documentation Rules

### 8.1 Code Documentation

- All Python functions must have Google-style docstrings
- All React components should have a JSDoc comment block describing purpose and props
- Complex algorithms must have inline comments explaining the approach
- Business logic decisions must be documented with `# Reason:` comments

### 8.2 Project Documentation

- All documentation files live in `docs/`
- Documentation must reflect the actual current state of the codebase
- Features must not be documented as "complete" unless code exists and works
- Update documentation when features are added, removed, or changed
- Use professional Markdown with tables, code blocks, and clear headings

---

## 9. File & Naming Rules

### 9.1 Backend (Python)

| Element | Convention | Example |
|---|---|---|
| Files | snake_case | `course_routes.py`, `llm_service.py` |
| Classes | PascalCase | `SessionStore`, `RAGService` |
| Functions | snake_case | `generate_course_pdf()` |
| Constants | UPPER_SNAKE_CASE | `SESSION_TTL`, `CHUNK_SIZE` |
| Route prefixes | kebab-case URL | `/generate-course` |
| Test files | `test_` prefix | `test_course_generator.py` |

### 9.2 Frontend (JavaScript/React)

| Element | Convention | Example |
|---|---|---|
| Component files | PascalCase.jsx | `MindmapFlow.jsx`, `FlashcardViewer.jsx` |
| Page files | lowercase.jsx or `[param].jsx` | `index.jsx`, `[id].jsx` |
| Utility files | camelCase.js | `convertMermaidToGraph.js`, `elkLayout.js` |
| Component exports | PascalCase default export | `export default MindmapFlow` |
| Props | camelCase | `onNodeClick`, `isFlipped`, `flashcardsData` |
| CSS classes | Tailwind utilities | `bg-gradient-to-r from-blue-600` |

### 9.3 Generated Files

| Type | Directory | Naming |
|---|---|---|
| PDFs | `backend/app/static/pdf/` | `course_{session_id}.pdf` |
| Mindmap images | `backend/app/static/mindmaps/` or `backend/static/mindmaps/` | `mindmap_{session_id}.png/svg` |
| Mermaid source | `backend/app/static/mindmaps/` | `mindmap_{session_id}.mmd` |
| RAG indices | `temp/` | `rag_index_{session_id}.json` |

---

## 10. Git & Workflow Rules

### 10.1 Version Control

- `.gitignore` must exclude: `venv/`, `node_modules/`, `.env`, `__pycache__/`, `temp/`, `*.pdf`, generated mindmap files
- Never commit API keys, secrets, or environment files
- Never commit `node_modules/` or `venv/`

### 10.2 Branch Strategy

Not currently defined. Recommended:

| Branch | Purpose |
|---|---|
| `main` | Stable, working code |
| `dev` | Integration branch for features |
| `feature/*` | Individual feature branches |
| `fix/*` | Bug fix branches |

### 10.3 Commit Messages

Not currently enforced. Recommended format:

```
type(scope): short description

feat(backend): add real LLM integration to llm_service
fix(frontend): resolve flashcard flip animation on Safari
docs: update architecture.md with database layer
```

---

> _These rules document the conventions and constraints that currently exist in the codebase, along with recommended practices for maintaining quality as the project grows._
