# Product Requirements Document (PRD)

> **Status:** Active  
> **Last Updated:** July 24, 2026  
> **Version:** 1.0

---

## Table of Contents

- [1. Project Vision](#1-project-vision)
- [2. Problem Statement](#2-problem-statement)
- [3. Target Users](#3-target-users)
- [4. User Personas](#4-user-personas)
- [5. Goals](#5-goals)
- [6. Features](#6-features)
- [7. User Journey](#7-user-journey)
- [8. Success Metrics](#8-success-metrics)
- [9. Future Scope](#9-future-scope)

---

## 1. Project Vision

CourseCraft-AI is an AI-powered learning platform that generates personalized, structured courses from any topic. Users enter a topic and receive a complete curriculum—organized by weeks and days—along with downloadable PDFs, interactive mindmaps, flashcards, assignments, and a RAG-powered AI teacher for Q&A.

The long-term vision is a self-contained, intelligent learning companion that adapts to any subject, difficulty level, and language.

---

## 2. Problem Statement

Creating structured educational content is time-consuming and requires domain expertise. Students and self-learners lack access to personalized curricula tailored to their skill level and preferred pace. Existing platforms offer rigid, pre-built courses that cannot be customized on demand.

CourseCraft-AI solves this by generating complete course structures from a single topic input, providing supplementary learning materials (flashcards, assignments, mindmaps), and enabling interactive Q&A against the generated content.

---

## 3. Target Users

| Audience Type | Description | Key Needs |
|---|---|---|
| Primary | Self-learners and students who want structured learning paths for any topic | Personalized course generation, downloadable materials, interactive study tools |
| Secondary | Educators and tutors who need to quickly scaffold course content | Rapid curriculum creation, PDF export, visual mindmaps for teaching |
| Tertiary | Developers and technical learners exploring new technologies | Code-oriented courses, programming-specific flashcards and assignments |

---

## 4. User Personas

### Persona 1: Ananya — The Self-Learner

| Attribute | Details |
|---|---|
| Role | College student, 2nd year Computer Science |
| Age Range | 18–22 |
| Technical Skill | Intermediate |
| Goals | Learn Python, Data Structures, and ML at her own pace with structured guidance |
| Pain Points | Free resources are scattered and unstructured; paid courses are expensive and rigid |
| How They Use the Product | Enters a topic → generates a course → downloads PDF → studies with flashcards → asks questions to AI teacher |

### Persona 2: Ravi — The Educator

| Attribute | Details |
|---|---|
| Role | High school computer science teacher |
| Age Range | 30–45 |
| Technical Skill | Basic to Intermediate |
| Goals | Quickly create lesson plans and visual aids for classroom teaching |
| Pain Points | Spends hours creating curriculum from scratch; needs visual mindmaps for students |
| How They Use the Product | Enters a topic → generates course → exports PDF for class → shares mindmap on projector → creates flashcards for revision |

---

## 5. Goals

### 5.1 Business Goals

- Deliver a functional AI-powered course generation platform
- Differentiate through personalized, on-demand curriculum creation
- Build a foundation that supports future monetization (premium features, user accounts)

### 5.2 User Goals

- Generate a complete, structured course from any topic in under 60 seconds
- Download course content as a professional PDF
- Visualize course structure through interactive mindmaps
- Study using auto-generated flashcards and assignments
- Ask questions and receive context-aware answers from an AI teacher

### 5.3 Technical Goals

- Clean, modular backend architecture (FastAPI) that separates routes, services, and models
- Mock-first development pattern that allows seamless swap to real LLM integration
- RAG pipeline architecture ready for production-grade embedding and vector store upgrades
- Frontend component system (React/Next.js) with reusable, composable components

---

## 6. Features

### 6.1 Feature Overview

| # | Feature | Priority | Phase | Current Status |
|---|---|---|---|---|
| 1 | Course Generation (JSON structure) | Critical | 1 | 🟡 Functional (mock AI) |
| 2 | PDF Generation | Critical | 1 | 🟡 Functional |
| 3 | RAG-Powered Q&A | Critical | 1 | 🟡 Functional (mock AI) |
| 4 | Session-Based Storage | High | 1 | 🟡 Functional (in-memory) |
| 5 | Mindmap Generation + Visualization | High | 2 | 🟢 Stable |
| 6 | Flashcard Generation + Viewer | High | 2 | 🟡 Functional (mock AI) |
| 7 | Assignment Generation + Viewer | High | 2 | 🟡 Functional (mock AI) |
| 8 | Difficulty Levels | Medium | 2 | 🟡 Functional |
| 9 | Course Generation Form (Frontend) | Critical | 1 | ❌ Missing |
| 10 | Course Content Viewer (Frontend) | Critical | 1 | ❌ Missing |
| 11 | AI Teacher Chat Interface | Critical | 1 | ❌ Missing |
| 12 | Real LLM Integration | Critical | 2 | ❌ Missing |
| 13 | Database / Persistence | Critical | 3 | ❌ Missing |
| 14 | Authentication & User Accounts | High | 3 | ❌ Missing |
| 15 | Study Plan Generator | Medium | 3 | ❌ Missing (stub files only) |
| 16 | Voice Mode (TTS + STT) | Low | 4 | ❌ Missing |
| 17 | Syllabus Alignment (PDF upload) | Low | 4 | ❌ Missing |
| 18 | Analytics Dashboard | Low | 4 | ❌ Missing |

### 6.2 Feature Details

#### Feature: Course Generation

| Attribute | Details |
|---|---|
| Description | Generate a complete course structure (weeks, days, objectives, content, activities) from a topic, duration, difficulty, and language |
| User Story | As a learner, I want to enter a topic and receive a structured course so that I can study systematically. |
| Acceptance Criteria | Returns valid JSON with course_id, title, weeks, days, assignments, and flashcards. Supports 1–24 week durations. Supports beginner/intermediate/advanced. |
| Current State | Implemented with mock LLM (deterministic template generation). Backend endpoint `/api/v1/generate-course` is active. **Frontend form to trigger generation is missing.** |

#### Feature: PDF Generation

| Attribute | Details |
|---|---|
| Description | Convert generated course JSON into a downloadable PDF document |
| User Story | As a learner, I want to download my course as a PDF so that I can study offline. |
| Acceptance Criteria | Generates valid PDF with title, description, objectives, week/day content, assignments, and flashcards |
| Current State | Fully functional using ReportLab. Pipeline: Course JSON → Markdown → ReportLab Story → PDF. Frontend button connected on `course/[id]` page. |

#### Feature: RAG Q&A

| Attribute | Details |
|---|---|
| Description | Ask questions about generated course content and receive context-aware answers |
| User Story | As a learner, I want to ask questions about my course and get relevant answers so that I can deepen my understanding. |
| Acceptance Criteria | Chunks course text, generates embeddings, retrieves relevant chunks via cosine similarity, and generates answers using retrieved context |
| Current State | Full RAG architecture implemented (chunking, mock embeddings, cosine similarity, top-k retrieval). Uses mock answer generation (keyword matching). **Frontend chat interface is missing.** |

#### Feature: Mindmap Visualization

| Attribute | Details |
|---|---|
| Description | Generate and display an interactive mindmap of the course structure |
| User Story | As a learner, I want to see my course as a visual mindmap so that I can understand the structure at a glance. |
| Acceptance Criteria | Generates Mermaid diagram from course data. Renders interactive visualization with zoom, pan, expand/collapse. |
| Current State | Most polished feature (~90% complete). Backend generates Mermaid text. Frontend uses ReactFlow + ELK.js for interactive visualization with custom Course/Week/Day nodes, sidebar, minimap. |

---

## 7. User Journey

### 7.1 Current Flow (What Works Today)

```
1. User opens landing page (index.jsx)
2. User enters session ID or clicks "Create New Course"
   ⚠️ BROKEN: Redirects to /course-builder which doesn't exist
   ⚠️ MISSING: No course generation form
3. If user has a session ID → can navigate to:
   a. /course/{session_id} → Generate PDF, Assignments, Flashcards
   b. /mindmap/{session_id} → Interactive mindmap viewer
```

### 7.2 Intended Full Flow (Once Complete)

| Step | User Action | System Response |
|---|---|---|
| 1 | Opens landing page | Displays CourseCraft-AI homepage with options |
| 2 | Clicks "Create New Course" | Shows course generation form (topic, duration, difficulty, language) |
| 3 | Submits form | Backend generates course via LLM, returns session_id + course JSON |
| 4 | Views course content | Course Viewer displays weeks, days, objectives, activities |
| 5 | Downloads PDF | Generates and serves downloadable PDF |
| 6 | Views mindmap | Interactive ReactFlow mindmap with expand/collapse |
| 7 | Generates flashcards | Topic-aware flashcard cards with flip, navigation |
| 8 | Generates assignments | MCQ, short answer, and long answer questions |
| 9 | Asks AI teacher | Chat interface with RAG-powered contextual answers |

---

## 8. Success Metrics

| Metric | Definition | Target | Current State |
|---|---|---|---|
| Course Generation Time | Time from topic input to course JSON response | < 30 seconds | ~100ms (mock data, not meaningful) |
| PDF Generation Time | Time from request to PDF file ready | < 10 seconds | ~1-2 seconds |
| RAG Answer Relevance | User-rated relevance of AI teacher answers | > 80% satisfaction | Not measurable (mock answers) |
| Mindmap Load Time | Time from request to interactive mindmap rendered | < 5 seconds | ~2-3 seconds |
| Feature Completion | % of planned v1 features implemented | 100% | ~35% |

---

## 9. Future Scope

| Idea | Rationale for Deferral | Potential Phase |
|---|---|---|
| Voice Mode (TTS + STT) | Requires speech APIs, adds complexity | Phase 4+ |
| Syllabus Alignment (PDF upload) | Requires PDF parsing + alignment logic | Phase 4+ |
| Analytics Dashboard | Requires user accounts and usage tracking | Phase 4+ |
| Multi-language content generation | Backend accepts language param but content is English-only | Phase 3 |
| Course collaboration/sharing | Requires user accounts first | Phase 4+ |
| Quiz gamification | Requires interactive quiz engine | Phase 4+ |
| Mobile app | Web app should be mature first | Phase 5+ |
| Course export to SCORM/LTI | Enterprise feature, requires spec compliance | Phase 5+ |

---

> _This document reflects the actual current state of the project as of July 24, 2026. Features marked as missing have zero implementation in the codebase._