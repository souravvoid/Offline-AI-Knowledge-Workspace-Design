# Product Requirements Document (PRD)

## Khoji — Offline AI Knowledge Workspace

**Version:** 1.0
**Status:** Draft for Review
**Target Market:** Students, Engineers, Researchers, Teachers, Knowledge Workers
**License:** AGPL-3.0 (core) / MIT (plugin SDK)

---

## Executive Summary

Khoji is a **local-first AI knowledge operating system** that transforms documents into a permanent, interconnected knowledge graph. It runs completely offline, uses specialized multi-agent AI, and stores everything as portable Markdown files.

Unlike document summarizers, Khoji grows smarter with every document — building cross-referenced concepts, auto-generating flashcards and quizzes, and remembering user corrections and preferences over time.

---

## Product Vision

> "The VS Code for Knowledge."

A local-first AI operating system that turns documents into a permanent, interconnected knowledge graph that grows smarter with every import.

---

## Target Audience

| Segment | Size | Willingness to Pay | Key Need |
|---------|------|-------------------|----------|
| Engineering Students | Very Large | Low-Medium | Textbook understanding, exam prep |
| Medical Students | Large | Medium | Dense material mastery, diagram extraction |
| Researchers | Medium | High | Paper management, citation extraction, privacy |
| Software Engineers | Large | Medium | Technical docs, architecture decisions, second brain |
| Professors/Teachers | Medium | Medium | Course material creation, quiz generation |
| Lifelong Learners | Large | Low-Medium | Personal knowledge management |

---

## Core Features (P0 — Must Have)

### 1. Multi-Format Document Upload
- **Supported formats:** PDF, PNG, JPG, WEBP, PPT, PPTX, DOC, DOCX, EPUB
- **Upload methods:** Drag & drop, file picker, clipboard paste
- **Batch upload:** Queue multiple documents
- **Size limit:** 200MB per file (configurable)

### 2. Multi-Agent AI Pipeline
- **OCR Agent:** Text extraction from scanned documents/images
- **Layout Agent:** Document structure analysis
- **Knowledge Extraction Agent:** Concept and relationship extraction
- **Reasoning Agent:** Summary, explanation, analogy generation
- **Flashcard Agent:** Auto-flashcard generation (cloze + Q&A)
- **Quiz Agent:** MCQ and varied question generation
- **Diagram Agent:** Mermaid diagram generation
- **Timeline Agent:** Chronological event extraction
- **Knowledge Graph Agent:** Cross-document concept merging

### 3. Document Workspace
- **Notes View:** AI-generated structured Markdown notes
- **Flashcards View:** Card list, filter by difficulty/tag, review mode
- **Quiz View:** Take quiz with timer, instant feedback, results
- **Mind Map View:** Interactive Mermaid diagram with zoom/pan
- **Timeline View:** Chronological event visualization
- **Important Questions:** Auto-generated comprehension questions
- **Outline Panel:** Document table of contents

### 4. AI Chat with Document Context
- Context-aware chat (knows which document is active)
- Streams responses token-by-token
- Cites sources with page numbers
- `/` commands for quick actions (/quiz, /flashcard, /summarize, /explain)
- Follow-up questions maintain context
- Chat history saved per document

### 5. Interactive Knowledge Graph
- Force-directed graph visualization
- Clickable concept nodes with detail panel
- Auto-discovers cross-document connections
- Node types with visual encoding (concept, formula, person, date, etc.)
- Search and filter within graph
- Layout algorithms (force, hierarchical, radial, timeline)
- Backlinks generated automatically in Markdown

### 6. Semantic Search (Cmd+K)
- Global search across all documents
- Local vector embeddings (384-dim, all-MiniLM-L6-v2)
- Hybrid search: vector + keyword (BM25)
- Results ranked by relevance, with snippets
- Filter by document, collection, date, type
- Search within specific document

### 7. Spaced Repetition
- SM-2 or FSRS algorithm
- Auto-scheduled flashcard reviews
- Rating: Again, Hard, Good, Easy
- Statistics: retention rate, cards studied, time spent
- Weak topic identification
- Daily review queue with notification

### 8. Full Offline Operation
- All AI processing runs locally
- No internet required for core features
- Models downloaded once, cached permanently
- Graceful degradation when models unavailable
- Works on 4GB RAM, CPU-only

### 9. AI Memory
- Remembers user corrections and applies them
- Tracks topic mastery and weak areas
- Learns user preferences (style, format, difficulty)
- Adapts explanations to user level
- Full transparency: user can view/edit/clear memory

### 10. Export
- **Markdown** with YAML frontmatter
- **Anki .apkg** package
- **PDF** formatted document
- **LaTeX** for academic writing
- **JSON** structured data
- **CSV** flashcards and quiz data
- **Plain text** for maximum portability

---

## Secondary Features (P1 — Should Have)

### 11. Collections
- User-created topic groupings
- Smart collections (auto-rule based, e.g., "all documents with tag #physics")
- Nested collections
- Drag & drop organization

### 12. Markdown Editor
- WYSIWYG + source mode toggle
- Markdown syntax highlighting
- Live preview
- Auto-save
- Find & replace

### 13. Settings & Configuration
- **General:** Theme (light/dark/system), language, font size, reading mode
- **Models:** OCR, embedding, LLM selection and download
- **Storage:** Data location, auto-export, cache management
- **Keyboard Shortcuts:** Full shortcut reference, customizable
- **Accessibility:** High contrast, large text, screen reader support

### 14. Dashboard / Home
- Recent documents (last 10)
- Due flashcard count
- Study statistics (cards reviewed, retention, streak)
- Quick actions (upload, review, quiz)
- Daily learning progress

### 15. History
- Document processing history
- Chat history
- Search history
- Review history
- Export history

### 16. Error States & Recovery
- OCR failure with actionable suggestions
- Model missing with download prompt
- Out of memory with low-memory mode suggestion
- Corrupted file with repair options
- Unsupported format with supported formats list
- Storage full with cleanup wizard

### 17. Keyboard-First Navigation
- All actions accessible via keyboard
- Cmd+K search as command palette
- Customizable keybindings
- VS Code-like command system

---

## Future Features (P2 — Roadmap)

### 18. Plugin System
- **Parser plugins** — Support more file formats
- **OCR plugins** — Alternative OCR engines
- **LLM plugins** — Alternative local models
- **Exporter plugins** — More export formats
- **Diagram plugins** — Graphviz, PlantUML, D2
- **Theme plugins** — Custom CSS themes
- **MCP providers** — External tool integration
- **Plugin Store** — Community plugin marketplace

### 19. Mobile Companion
- Sync via LAN/local network (no cloud!)
- Review flashcards on mobile
- View notes
- Voice input for quick notes
- Camera import (take photo of document page)

### 20. Browser Extension
- Save web pages as documents
- Highlight and save excerpts
- Quick search from browser
- Side panel for Khoji access

### 21. Git Integration
- Auto-commit knowledge base changes
- Version history for notes
- Collaboration via Git
- PR-based knowledge review

### 22. Offline Collaboration
- LAN peer-to-peer sync
- Shared collections
- Collaborative quiz creation
- Shared flashcard review sessions

### 23. AI Tutoring Mode
- Adaptive learning paths based on knowledge graph
- Generates personalized study plans
- Suggests next documents to read based on weak areas
- Step-by-step problem-solving tutor

### 24. Research Workspace
- Literature review automation
- Citation graph extraction
- Systematic review support
- Paper comparison matrix
- BibTeX export

---

## Non-Functional Requirements

### Performance

| Metric | Target |
|--------|--------|
| Startup time | <3s cold, <1s warm |
| Document list render | <100ms (100 items) |
| Search results | <50ms (local vector search) |
| Flashcard flip | <16ms (60fps) |
| Processing (100pg PDF) | <120s (1B model) |
| AI Chat first token | <100ms (1B model) |
| Export (Markdown, 100pg) | <500ms |
| Memory (idle) | <200MB |
| Memory (processing) | <1GB |
| Disk (base) | <1GB |
| Disk (with small LLM) | <2GB |

### Security & Privacy

- All data stays on device
- No telemetry (opt-in crash reports only)
- No analytics
- No cloud dependencies
- File encryption (optional, for sensitive documents)
- Sandboxed plugin execution

### Accessibility (WCAG 2.1 AA)

- Keyboard navigable
- Screen reader compatible (ARIA labels)
- High contrast mode
- Font size: 100%–200%
- Motion reduction support
- Skip to content link
- Visible focus indicators

### Platform Support

| Platform | Support |
|----------|---------|
| Windows 10+ | ✅ Primary |
| macOS 12+ | ✅ Primary |
| Linux (x86_64) | ✅ Primary |
| Linux (arm64) | ⚠️ Secondary |
| Web | ❌ (deliberately offline-native) |
| iOS/Android | 📋 Roadmap |

---

## Technical Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Desktop Framework | **Tauri v2** | Small binary, Rust backend, cross-platform |
| Frontend | **React + TypeScript** | Large ecosystem, virtual DOM, hooks |
| Styling | **Tailwind CSS** | Design tokens, consistent, fast |
| State | **Zustand** | Simple, performant, TypeScript-native |
| Markdown | **remark + rehype** | Extensible Markdown pipeline |
| Mermaid | **mermaid.js** | Diagram rendering |
| Icons | **Lucide** | Consistent, open source |
| PDF Parsing | **pdf-extract + pdf.js** | Rust + JS combo |
| OCR | **Tesseract v5** (via tesseract-rs) | Mature, fast, 100+ languages |
| Embeddings | **all-MiniLM-L6-v2** (via ONNX) | Small, fast, good quality |
| Vector DB | **SQLite + sqlite-vec** | Embedded, no separate server |
| LLM | **llama.cpp** bindings (via llama-rs) | Best local LLM inference |
| Database | **SQLite** | Embedded, reliable, zero-config |
| Graphs | **D3.js** (force-directed) + **Cytoscape.js** | Interactive graph rendering |

---

## Success Metrics

| Metric | Target (3 months post-launch) |
|--------|-------------------------------|
| GitHub Stars | 5,000+ |
| Active users | 1,000+ |
| Documents processed | 10,000+ |
| User retention (weekly) | 40%+ |
| NPS | 50+ |
| Plugin count (community) | 20+ |
| Average processing time | <60s per 100pg doc |
