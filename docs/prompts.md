# Prompt Library

> **Status:** Draft
> **Last Updated:** _(date)_
> **Author:** _(name)_

---

## Table of Contents

- [1. Master Prompt](#1-master-prompt)
- [2. Backend Prompt](#2-backend-prompt)
- [3. Frontend Prompt](#3-frontend-prompt)
- [4. UI Prompt](#4-ui-prompt)
- [5. Bug Fix Prompt](#5-bug-fix-prompt)
- [6. Refactoring Prompt](#6-refactoring-prompt)
- [7. Review Prompt](#7-review-prompt)

---

## How to Use This Document

<!-- Explain how and when to use these prompts, and the conventions for updating them. -->

| Convention | Description |
|---|---|
| Variables | Use `{{variable_name}}` for dynamic values |
| Sections | Each prompt is self-contained and can be used independently |
| Updates | Always update the "Last Updated" date when modifying a prompt |
| Testing | Test prompts before committing changes |

---

## 1. Master Prompt

> **Purpose:** The foundational prompt that sets the context and rules for all AI interactions across the project.
> **When to Use:** At the start of every AI-assisted coding session.

### System Context

```
{{master_prompt_content}}
```

### Key Rules

- 
- 
- 

### Project Context Block

```
{{project_context}}
```

---

## 2. Backend Prompt

> **Purpose:** Prompt for AI-assisted backend development.
> **When to Use:** When working on API routes, services, models, or backend logic.

### System Context

```
{{backend_prompt_content}}
```

### Scope

- 
- 
- 

### Constraints

- 
- 
- 

### Output Format

```
{{expected_output_format}}
```

---

## 3. Frontend Prompt

> **Purpose:** Prompt for AI-assisted frontend development.
> **When to Use:** When working on pages, components, layouts, or client-side logic.

### System Context

```
{{frontend_prompt_content}}
```

### Scope

- 
- 
- 

### Constraints

- 
- 
- 

### Output Format

```
{{expected_output_format}}
```

---

## 4. UI Prompt

> **Purpose:** Prompt for AI-assisted UI/UX design and styling.
> **When to Use:** When designing new components, screens, or refining visual styles.

### System Context

```
{{ui_prompt_content}}
```

### Design References

<!-- Link to design system or reference materials. -->

- 
- 

### Constraints

- 
- 
- 

### Output Format

```
{{expected_output_format}}
```

---

## 5. Bug Fix Prompt

> **Purpose:** Prompt for AI-assisted debugging and bug fixing.
> **When to Use:** When diagnosing and resolving bugs.

### System Context

```
{{bug_fix_prompt_content}}
```

### Required Input

| Field | Description |
|---|---|
| Bug Description | |
| Steps to Reproduce | |
| Expected Behavior | |
| Actual Behavior | |
| Error Logs | |
| Affected Files | |

### Constraints

- 
- 
- 

### Output Format

```
{{expected_output_format}}
```

---

## 6. Refactoring Prompt

> **Purpose:** Prompt for AI-assisted code refactoring and cleanup.
> **When to Use:** When improving code quality without changing functionality.

### System Context

```
{{refactoring_prompt_content}}
```

### Required Input

| Field | Description |
|---|---|
| Target Files | |
| Refactoring Goal | |
| Constraints | |

### Quality Checklist

- [ ] No behavioral changes
- [ ] All tests pass
- [ ] Code is more readable
- [ ] Follows project conventions
- [ ] No new dependencies introduced

### Output Format

```
{{expected_output_format}}
```

---

## 7. Review Prompt

> **Purpose:** Prompt for AI-assisted code review.
> **When to Use:** Before merging code or after completing a feature.

### System Context

```
{{review_prompt_content}}
```

### Review Criteria

| Category | What to Check |
|---|---|
| Correctness | |
| Performance | |
| Security | |
| Readability | |
| Conventions | |
| Edge Cases | |
| Tests | |

### Severity Levels

| Level | Label | Description |
|---|---|---|
| 🔴 | Critical | |
| 🟡 | Suggestion | |
| 🟢 | Nitpick | |
| 💡 | Idea | |

### Output Format

```
{{expected_output_format}}
```

---

## Prompt Changelog

| Date | Prompt | Change Description | Author |
|---|---|---|---|
| | | | |
| | | | |

---

> _This prompt library is the single source of truth for all AI interactions in this project. Always use the latest version._
