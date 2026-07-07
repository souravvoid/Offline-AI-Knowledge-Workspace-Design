# Khoji Desktop — Design Specification (`design.md`)

This document outlines the visual system, user experience logic, and architectural designs implemented for the **Khoji Offline AI Knowledge Workspace** documentation portal.

---

## 1. Product Vision & Design Principles

> **"The VS Code for Knowledge"**
> A local-first, offline AI knowledge operating system that turns documents into a permanent, interconnected knowledge graph that grows smarter with every import.

The design of the portal directly mirrors this vision. Instead of using generic marketing templates, the layout is organized around the **native shape** of the product: a **linear processing pipeline** and a **relational network of database schemas**.

### Core Constraints & Rationale
- **Zero Cloud Reliance (Offline-Native):** All scripts, stylesheets, and assets are local. Standard icons are built as inline SVGs rather than loading external CDNs.
- **Truthful Content (No Placeholders):** Every copy fragment, database column, model preset, and keyboard shortcut is pulled directly from the active code base.
- **Micro-Animations & Rich Aesthetics:** High-contrast dark backgrounds, glowing glassmorphic elements, and smooth interactive spring curves present a premium desktop-grade feel.

---

## 2. Visual Identity & Design Tokens

The visual design system inherits the specifications outlined in the project's design files (`design/26-design-tokens.md` and `theme.py`).

### Color System (Light/Dark Schemes)

| Token Key | Light Theme Value | Dark Theme Value | Purpose |
|:---|:---|:---|:---|
| `bg_primary` | `#FFFFFF` | `#0F172A` | Primary canvas background |
| `bg_secondary` | `#F8FAFC` | `#1E293B` | Sidebar, secondary panels, inputs |
| `bg_tertiary` | `#F1F5F9` | `#334155` | Code containers, badges, scroll track |
| `border` | `#E2E8F0` | `#334155` | Default separator borders |
| `border_hover` | `#CBD5E1` | `#475569` | Interactive element hover states |
| `text_primary` | `#0F172A` | `#F1F5F9` | Primary headlines and labels |
| `text_secondary`| `#475569` | `#94A3B8` | Subheadings and body copy |
| `text_tertiary` | `#94A3B8` | `#64748B` | Disabled indicators, inline comments |
| `accent` | `#6366F1` | `#818CF8` | Indigo accent colors (buttons, toggles) |
| `accent_hover` | `#4F46E5` | `#6366F1` | Accent color hover states |

### Spacing & Layout
- **Grid base:** Built on a 4px increment scale (e.g. `--space-1` = 4px, `--space-4` = 16px, `--space-8` = 32px).
- **Border Radii:** Rounded cards `radius-lg` (12px), inputs `radius-md` (8px), and overlay dialogs `radius-xl` (16px).
- **Typographic Hierarchy:**
  - Font Families: `Inter` (sans-serif UI), `JetBrains Mono` (code structures), `Source Serif 4` (notes reading view).
  - Scale: `h1` = 36px (700 weight), `h2` = 24px (600 weight), `h3` = 20px (600 weight), `body` = 16px.

---

## 3. Interactive Components Architecture

The documentation portal incorporates dynamic, responsive features constructed with Vanilla HTML/CSS/JS:

```
┌────────────────────────────────────────────────────────┐
│                      HEADER NAV                        │
│  [Logo] Khoji       [Search Docs...]    [Theme Switch] │
├─────────────────────────┬──────────────────────────────┤
│                         │                              │
│  SIDEBAR MENU           │  DOCS CANVAS                 │
│                         │                              │
│  1. Ingestion / Setup ──┼─► Terminal CLI Copy          │
│  2. PRD Specs           │                              │
│  3. Multi-Agent Flow ───┼─► Horizontal Pipeline Map    │
│  4. Database Design ────┼─► Schema Code Explorer       │
│  5. AI Memory System ───┼─► JSON State Toggle          │
│  6. Shortcuts & Access  │                              │
│                         │                              │
└─────────────────────────┴──────────────────────────────┘
```

### 3.1. Theme Toggle & FOUC Prevention
To respect system color schemes and prevent Flash of Unstyled Content (FOUC), an inline script immediately reads from `localStorage` keys and sets the `data-theme` attribute on document headers before rendering body layouts:
```html
<script>
  const colorScheme = localStorage.getItem('color-scheme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', colorScheme);
</script>
```

### 3.2. Multi-Agent Pipeline Map
Visualizes the 12 specialized agents coordinated by the background processor thread.
- **User Interface:** A horizontal progress tracker mapping Ingestion -> Extraction -> Indexing -> Synthesis -> Export.
- **Dynamic Routing:** Clicking a step updates the agent grid below, highlighting active models, inputs/outputs, and RAM presets (Low vs High RAM configurations).

### 3.3. SQLite Database Schema Explorer
Developers can inspect relational structures without opening a terminal terminal:
- **Left Panel:** Table selections (`documents`, `document_chunks`, `flashcards`, `ai_memory`, `chunk_embeddings` vectors).
- **Right Panel:** Standardized DDL schema with syntax coloring and indices (WAL mode structures).

### 3.4. AI Memory JSON Viewer
Shows exact JSON structures RAG agents reference to adapt outputs to users:
- **Tabs:** Concept, Preference, Progress, Interaction, and Correction memories.
- **Behavioral changes:** Details on how memory alters chat streaming, flashcard difficulties, and summaries.

---

## 4. Accessibility (WCAG 2.1 AA) & Performance Targets

### Accessibility Compliance
- **Contrast Ratios:** Minimum contrast ratio of 4.5:1 (targets 7.8:1 in dark mode) for all text labels.
- **Focus Rings:** Explicit 2px indigo outline focus indicators on input fields.
- **Motion Reduction:** Full CSS media queries respecting system prefers-reduced-motion profiles.

### Performance Latency Budgets
- **Startup:** `< 3s` cold start, `< 1s` warm launch.
- **Vector search:** `< 50ms` RAG local index search response times.
- **Rendering:** `< 100ms` for document grids of up to 100 library files.
