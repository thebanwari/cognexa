# Design System

> **Status:** Active  
> **Last Updated:** July 24, 2026  
> **Version:** 1.0

---

## Table of Contents

- [1. Design Philosophy](#1-design-philosophy)
- [2. Color Palette](#2-color-palette)
- [3. Typography](#3-typography)
- [4. Spacing](#4-spacing)
- [5. Shadows](#5-shadows)
- [6. Border Radius](#6-border-radius)
- [7. Components](#7-components)
- [8. Icons](#8-icons)
- [9. Animations](#9-animations)
- [10. Responsive Rules](#10-responsive-rules)
- [11. Accessibility](#11-accessibility)

---

## 1. Design Philosophy

### 1.1 Core Principles

- **Clarity over decoration:** Content-first layouts where course material and visualizations take center stage
- **Progressive disclosure:** Expand/collapse patterns for weeks/days in mindmaps, expandable answers in assignments
- **Gradient-heavy accents:** Gradient backgrounds and buttons used consistently for visual hierarchy
- **Functional color coding:** Course (indigo), Week (green), Day (amber) — applied consistently across mindmap nodes, buttons, and badges

### 1.2 Design Goals

- Make generated educational content feel professional and trustworthy
- Provide intuitive navigation between course output types (PDF, mindmap, flashcards, assignments)
- Support focused, distraction-free study experiences (full-screen mindmap, flip-card flashcards)

### 1.3 Visual Identity

- **Tone:** Clean, modern, educational — professional but not corporate
- **Background:** Gradient canvas (`from-blue-50 via-indigo-50 to-purple-50`) used on main pages
- **Cards:** White cards with rounded corners, subtle shadows, and light borders
- **Buttons:** Bold gradient fills with hover scale transforms for primary actions

---

## 2. Color Palette

### 2.1 Course/Node Palette (Tailwind Custom)

Defined in `tailwind.config.js` as custom color scales:

| Name | Shade | Hex | Usage |
|---|---|---|---|
| `course-50` | Lightest | `#eef2ff` | Course node background |
| `course-100` | | `#e0e7ff` | Course node hover |
| `course-200` | | `#c7d2fe` | Course accent borders |
| `course-500` | Primary | `#6366f1` | Course badges, spinners |
| `course-600` | | `#4f46e5` | Course buttons |
| `course-700` | Dark | `#4338ca` | Course button hover |
| `week-50` | Lightest | `#ecfdf5` | Week node background |
| `week-100` | | `#d1fae5` | Week node hover |
| `week-200` | | `#a7f3d0` | Week accent borders |
| `week-500` | Primary | `#10b981` | Week badges |
| `week-600` | | `#059669` | Week buttons |
| `week-700` | Dark | `#047857` | Week button hover |
| `day-50` | Lightest | `#fffbeb` | Day node background |
| `day-100` | | `#fef3c7` | Day node hover |
| `day-200` | | `#fde68a` | Day accent borders |
| `day-500` | Primary | `#f59e0b` | Day badges |
| `day-600` | | `#d97706` | Day buttons |
| `day-700` | Dark | `#b45309` | Day button hover |
| `canvas-50` | | `#f8fafc` | Canvas background |
| `canvas-100` | | `#f1f5f9` | Canvas secondary |
| `canvas-200` | | `#e2e8f0` | Canvas borders |

### 2.2 Standard Tailwind Colors in Use

| Purpose | Color Classes Used |
|---|---|
| Primary actions | `from-blue-600 to-indigo-600`, `from-blue-600 to-blue-700` |
| Success / "View Mindmap" | `from-green-600 to-emerald-600` |
| Flashcards / Purple actions | `from-purple-500 to-purple-600`, `from-purple-600 to-purple-700` |
| Assignments | `from-green-500 to-green-600` |
| Error states | `bg-red-50 border-red-200 text-red-700` |
| Success states | `bg-green-50 border-green-200 text-green-700` |
| Text primary | `text-gray-900` |
| Text secondary | `text-gray-600` |
| Text muted | `text-gray-400`, `text-gray-500` |
| Borders | `border-gray-200`, `border-gray-100` |
| Background | `bg-white`, `bg-gray-50`, `bg-gray-100` |

### 2.3 Semantic Colors

| Name | Color | Usage |
|---|---|---|
| Success | Green-50/200/600/700 | PDF generated successfully, valid states |
| Error | Red-50/200/500/700 | Generation failures, error banners |
| Info | Blue-50/500 | Information badges, answer highlights |
| Warning | Amber/Yellow | Not explicitly used in current components |

### 2.4 Dark Mode

Not implemented. All pages use light mode only.

---

## 3. Typography

### 3.1 Font Families

| Role | Font Family | Fallback Stack |
|---|---|---|
| Sans-serif (primary) | Inter | system-ui, -apple-system, sans-serif |
| Monospace | JetBrains Mono | Fira Code, monospace |

Defined in `tailwind.config.js` under `fontFamily`.

### 3.2 Type Scale (Tailwind Classes in Use)

| Name | Tailwind Class | Usage |
|---|---|---|
| Page title | `text-4xl font-bold` | Main headings on landing, course pages |
| Section title | `text-3xl font-bold` | Brand name in header |
| Component heading | `text-2xl font-bold` | Placeholder page titles |
| Card heading | `text-xl font-semibold` | Section headers (assignments, instructions) |
| Subsection | `text-lg font-semibold` | Feature card titles, instructions heading |
| Body | `text-base` (default) | Paragraph text |
| Small body | `text-sm` | Feature descriptions, helper text |
| Tiny labels | `text-xs`, `text-[11px]` | Legends, session IDs, minimap labels |

### 3.3 Font Weights

| Name | Weight | Usage |
|---|---|---|
| Regular | 400 | Body text, descriptions |
| Medium | 500 | `font-medium` — input labels, subtitles |
| Semi-Bold | 600 | `font-semibold` — buttons, card titles |
| Bold | 700 | `font-bold` — page titles, brand |

---

## 4. Spacing

### 4.1 Spacing Scale (Tailwind Default)

The project uses standard Tailwind spacing. Most common values used:

| Token | Value | Usage |
|---|---|---|
| `1` | 4px | Fine spacing (gap-1, space-x-1) |
| `2` | 8px | Small gaps between icons and text |
| `3` | 12px | Button padding (py-3) |
| `4` | 16px | Card inner padding, section gaps |
| `6` | 24px | Page horizontal padding (px-6), card padding (p-6) |
| `8` | 32px | Card large padding (p-8), section vertical spacing |
| `12` | 48px | Page vertical padding (py-12) |
| `16` | 64px | Large section gaps (mt-16) |

### 4.2 Layout Spacing

| Context | Value | Notes |
|---|---|---|
| Page max width | `max-w-4xl` or `max-w-6xl` | Centered with `mx-auto` |
| Page horizontal padding | `px-6` | Consistent across pages |
| Page vertical padding | `py-12` | Main content area |
| Card padding | `p-6` to `p-8` | White card containers |
| Button padding | `py-2 px-4` to `py-4 px-8` | Varies by importance |
| Form field gap | `mb-4` | Between label and input |
| Grid gap | `gap-6` to `gap-8` | Feature cards, action buttons |

---

## 5. Shadows

| Name | Value | Usage |
|---|---|---|
| `shadow-lg` | Tailwind default | Cards, buttons, feature tiles |
| `shadow-xl` | Tailwind default | Hover states on buttons |
| `shadow-node` | `0 4px 20px rgba(0,0,0,0.08)` | Mindmap node default (custom) |
| `shadow-node-hover` | `0 8px 30px rgba(0,0,0,0.12)` | Mindmap node hover (custom) |
| `shadow-node-active` | `0 2px 10px rgba(0,0,0,0.05)` | Mindmap node pressed (custom) |
| `shadow-glass` | `0 8px 32px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.6)` | Glassmorphism effect (custom) |

---

## 6. Border Radius

| Usage | Tailwind Class | Approximate Value |
|---|---|---|
| Small buttons | `rounded-lg` | 8px |
| Cards, inputs | `rounded-xl` | 12px |
| Large cards, modals | `rounded-2xl` | 16px |
| Badges, pills | `rounded-full` | 9999px |
| Mindmap nodes | `rounded-xl` to `rounded-2xl` | 12–16px |

---

## 7. Components

### 7.1 Component Inventory

| Component | Status | Variants | States |
|---|---|---|---|
| Action Button (gradient) | ✅ Implemented | Blue, Green, Purple gradients | Default, Hover (scale-105), Loading (spinner), Disabled |
| Card | ✅ Implemented | White with border, Gradient header | Default, Hover (shadow) |
| Input | ✅ Implemented | Text input with label | Default, Focus (ring-2 ring-blue-500) |
| Error Banner | ✅ Implemented | Red themed | Visible/hidden |
| Success Banner | ✅ Implemented | Green themed | Visible/hidden |
| Loading Spinner | ✅ Implemented | Circular border spinner | Animated spin |
| Flashcard | ✅ Implemented | Front/Back flip | Flipped/unflipped, cursor-pointer |
| Assignment Question | ✅ Implemented | MCQ, SHORT, LONG types | Expanded/collapsed |
| Mindmap Node | ✅ Implemented | Course, Week, Day types | Default, Hover, Selected, Expanded/Collapsed |
| Sidebar Panel | ✅ Implemented | Slide-in from right | Open/closed |
| Modal | ✅ Implemented | Flashcard modal with overlay | Open/closed, Loading, Error |
| Course Form | ❌ Missing | — | — |
| Course Viewer | ❌ Missing | — | — |
| Chat Interface | ❌ Missing | — | — |
| Navigation/Header | ❌ Missing (no shared nav) | — | — |

### 7.2 Button Specifications (As Implemented)

| Variant | Background | Text | Hover | Active |
|---|---|---|---|---|
| Primary (Blue) | `from-blue-600 to-indigo-600` | White | `from-blue-700 to-indigo-700` + `scale-105` | — |
| Secondary (Green) | `from-green-600 to-emerald-600` | White | `from-green-700 to-emerald-700` + `scale-105` | — |
| Accent (Purple) | `from-purple-600 to-purple-700` | White | Darker gradient + `scale-105` | — |
| Ghost/Back | `bg-transparent` or `bg-gray-100` | `text-gray-500` | `bg-gray-100` + `text-gray-700` | — |
| Disabled | `bg-gray-100` | `text-gray-400` | `cursor-not-allowed`, no hover | — |

### 7.3 Mindmap Node Specifications

| Node Type | Background | Border Accent | Size | Special |
|---|---|---|---|---|
| CourseNode | White/glass | Indigo left border | Largest | Gradient icon, glow animation |
| WeekNode | White/glass | Green left border | Medium | Expand/collapse chevron button |
| DayNode | White/glass | Amber left border | Smallest | Staggered entrance animation via `--day-index` CSS var |

---

## 8. Icons

### 8.1 Icon Library

| Attribute | Value |
|---|---|
| Library | Heroicons (inline SVG, not imported as package) |
| Method | Hand-coded `<svg>` elements directly in JSX |
| Default Size | `w-5 h-5` (20×20px) |
| Default Stroke Width | `2` |
| Color Inheritance | Yes — uses `currentColor` via `stroke="currentColor"` |

### 8.2 Icon Usage

| Context | Size | Color |
|---|---|---|
| Button inline icons | `w-5 h-5` | White (on gradient buttons) |
| Feature card icons | `w-10 h-10` | Blue/Indigo/Purple |
| Header logo icon | `w-5 h-5` to `w-10 h-10` | White on gradient circle |
| Error/success banner | `w-5 h-5` | Red-500 / Green-500 |
| Navigation | `w-5 h-5` | Gray-500 |

---

## 9. Animations

### 9.1 Timing & Easing (Custom Tailwind)

| Name | Duration | Easing | Usage |
|---|---|---|---|
| `fade-in` | 300ms | ease-out | Node entrance, component mount |
| `slide-in-right` | 300ms | ease-out | Sidebar panel appearance |
| `pulse-soft` | 3s | ease-in-out | Subtle background pulse (infinite) |
| `glow` | 2s | ease-in-out | Course node glow effect (infinite) |

### 9.2 Transition Defaults (CSS Classes Used)

| Property | Duration | Easing | Tailwind Class |
|---|---|---|---|
| Colors | 200ms | default | `transition-colors` |
| All properties | 200–300ms | default | `transition-all duration-200` / `duration-300` |
| Transform | 200ms | default | `transform hover:scale-105` |
| Box Shadow | 300ms | default | `transition-shadow` |

### 9.3 Keyframe Definitions

```css
/* From tailwind.config.js */
fadeIn:        0% → opacity:0, scale(0.95)  →  100% → opacity:1, scale(1)
slideInRight:  0% → opacity:0, translateX(20px)  →  100% → opacity:1, translateX(0)
pulseSoft:     0%,100% → opacity:1  →  50% → opacity:0.85
glow:          0%,100% → boxShadow: 0 0 20px rgba(99,102,241,0.15)
               50% → boxShadow: 0 0 40px rgba(99,102,241,0.3)
```

### 9.4 Special Animations

- **Flashcard flip:** CSS 3D transform with `rotateY(180deg)`, `perspective-1000`, `backface-visibility:hidden`
- **Day node stagger:** Uses CSS custom property `--day-index` for cascaded entrance timing
- **Loading spinner:** Standard Tailwind `animate-spin` with border-b-2 circle
- **ELK layout transition:** `fitView()` with `duration: 550-650ms` for camera animation on expand/collapse

---

## 10. Responsive Rules

### 10.1 Breakpoints

Standard TailwindCSS breakpoints used:

| Name | Min Width | Usage in Codebase |
|---|---|---|
| `sm` | 640px | `sm:space-x-4`, `sm:flex-row` — button layouts switch from stack to row |
| `md` | 768px | `md:grid-cols-3` — feature cards from 1 to 3 columns |
| `lg` | 1024px | Not explicitly used |
| `xl` | 1280px | Not explicitly used |

### 10.2 Responsive Patterns

| Pattern | Behavior |
|---|---|
| Action buttons | Stack vertically on mobile (`flex-col`), row on `sm:` (`sm:flex-row sm:space-x-4`) |
| Feature grid | Single column → 3 columns at `md:` |
| Mindmap legend | Hidden on mobile, visible on `sm:` (`hidden sm:flex`) |
| Page container | Consistent `max-w-4xl mx-auto px-6` across breakpoints |
| Mindmap | Full screen (`h-screen`) regardless of viewport |

### 10.3 Touch Targets

| Element | Minimum Size |
|---|---|
| Primary buttons | `py-4 px-8` (~48px height) — meets 44px minimum |
| Navigation buttons | `py-1.5 px-3` (~28px height) — below recommended 44px minimum |
| Flashcard dot indicators | `w-3 h-3` (12px) — below recommended 44px touch target |

---

## 11. Accessibility

### 11.1 Current State

Accessibility has **not been systematically addressed**. The following is an assessment of what exists:

| Attribute | Current Value |
|---|---|
| Target WCAG Level | Not defined |
| Color Contrast (text on backgrounds) | Generally passes (gray-900 on white), but gradient buttons need verification |
| Semantic HTML | Partial — uses `<header>`, `<button>`, but no `<nav>`, `<main>`, `<section>` |
| Keyboard navigation | Flashcard viewer supports keyboard (←→ Space). Mindmap does not. |
| ARIA labels | Not implemented |
| Alt text | SVG icons lack `aria-label` |
| Focus states | Tailwind `focus:ring-2 focus:ring-blue-500` on input. Buttons lack explicit focus styles. |
| Screen reader support | Not implemented |

### 11.2 Accessibility Gaps

- No `aria-label` on any interactive SVG icon
- No skip-to-content link
- No `<main>` landmark on any page
- Flashcard card dot indicators (12px) are below touch target minimums
- Color-only distinction for MCQ/SHORT/LONG assignment types (no text labels visible when collapsed)
- No reduced-motion media query handling for animations

---

> _This design system documents the visual decisions as they currently exist in the codebase. All values are derived from `tailwind.config.js`, `globals.css`, and component source code._
