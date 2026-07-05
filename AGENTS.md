# Khoji — AGENTS.md

Product: **Khoji** (खोजी) — Offline AI Knowledge Workspace.
Goal: Desktop app (Tauri + React/Rust) where users upload documents → local AI produces structured knowledge (notes, flashcards, quiz, mind map, chat, knowledge graph).

## State of the repo

**Design phase only. No code exists yet.** All decisions below are from `design/` and must be honored during implementation.

## Design source of truth

`design/` contains 30 complete design documents. Key files for implementation:

| File | What it tells you |
|------|-------------------|
| `28-hackathon-mvp-scope.md` | **Start here.** P0/P1/P2 breakdown, 3-day plan, team roles |
| `17-prd.md` | Full feature spec, non-functional requirements, tech stack |
| `11-architecture.md` | System architecture, folder structure, component diagram |
| `05-design-system.md` | Light/dark theme, typography, spacing, component specs |
| `18-implementation-roadmap.md` | Phased build plan (14 weeks) |
| `27-acceptance-criteria.md` | Pass/fail criteria per feature |

## Tech stack (locked)

| Layer | Choice | Why |
|-------|--------|-----|
| Desktop | **Tauri v2** | Small binary, Rust backend, cross-platform |
| Frontend | **React + TypeScript + Vite** | Fast setup, large ecosystem |
| Styling | **Tailwind CSS** | Design tokens, consistent |
| State | **Zustand** | Simple, TypeScript-native |
| Backend | **Rust** (via Tauri) | Safe, fast, native AI integration |
| OCR | **Tesseract v5** | Mature, 100+ languages, offline |
| Embeddings | **all-MiniLM-L6-v2** (ONNX) | 80MB, 384-dim, CPU-friendly |
| LLM | **Llama 3.2 1B** (llama.cpp, GGUF) | 620MB Q4_K_M, 1-2GB RAM |
| Vector DB | **SQLite + sqlite-vec** | Embedded, zero-config |
| Diagrams | **Mermaid.js** | Renders in Markdown |
| Icons | **Lucide React** | Consistent, open source |

## Architecture essentials

```
src/
├── frontend/          # React UI
│   ├── components/    # 60+ components (see 25-ui-component-library.md)
│   ├── hooks/         # useDocuments, useSearch, useChat, useProcessing
│   ├── stores/        # Zustand stores (document, ui, chat, review, settings)
│   └── lib/           # IPC wrapper, markdown, mermaid, keyboard utils
└── backend/           # Tauri/Rust
    ├── commands/      # IPC handlers (upload, process, search, chat, export)
    ├── pipeline/      # orchestrator, parser, ocr, chunker, embedder, llm
    ├── db/            # SQLite schema, migrations
    ├── models/        # AI model interfaces (ocr, embedding, llm)
    └── export/        # markdown, anki, pdf, latex, json, csv
```

All IPC calls are `invoke('command_name', {args})` — see `19-api-specification.md` for every command signature.

## Multi-agent AI pipeline

Never use one model for everything. The pipeline chains 12 specialized agents (see `12-multi-agent-system.md`):

```
PDF → [OCR] → [Layout] → [Vision] → [Knowledge Extraction] → [Reasoning]
      → [Knowledge Graph] → [Flashcard] → [Quiz] → [Diagram] → [Markdown] → [Export]
```

Each agent has a dedicated prompt in `24-prompt-engineering-guide.md`.

## MVP build order (3-day hackathon)

From `28-hackathon-mvp-scope.md`:

1. **Day 1:** Tauri + React setup, AppShell, Library view, Upload zone
2. **Day 2:** PDF text extraction, OCR, Markdown generation, Notes tab, Export, Processing UI
3. **Day 3:** Embeddings, Semantic search, AI Chat, Flashcards, Quiz, Polish

Pre-download before building: Tesseract (50MB), MiniLM ONNX (80MB), Llama 3.2 1B GGUF (620MB).

## Database

SQLite at `~/.khoji/db/khoji.db`. Full schema in `20-database-design.md`. Key tables: `documents`, `document_chunks`, `notes`, `flashcards`, `flashcard_reviews`, `quiz_questions`, `concepts`, `concept_relationships`, `chat_sessions`, `chat_messages`, `ai_memory`, `ai_corrections`, `user_settings`.

Vector embeddings in separate `vectors.db` via sqlite-vec virtual table.

## Security model

- 100% local. No telemetry. No cloud.
- Plugin sandboxing via WASM (wasmtime).
- Prompt injection defense via input sanitization + prompt isolation.
- All model downloads verified via SHA256.

See `22-security-document.md`.

## Testing

See `23-testing-strategy.md`. Pyramid: static analysis → unit tests → integration → E2E.
CI runs: `cargo clippy`, `cargo test`, `npm run lint`, `npm run test:unit`, `npm run typecheck`.

## Design doc index

```
01  Problem Understanding & Vision
02  User Personas (5)
03  User Journeys (6)
04  Information Architecture
05  Design System & Color Palette
06  Wireframes (13 screens)
07  Animations & AI Experience
08  Markdown Design & Mermaid
09  Accessibility & Performance
10  Empty & Error States
11  Architecture Diagrams
12  Multi-Agent System
13  Interactive Knowledge Graph
14  AI Memory System
15  Plugin Architecture & SDK
16  Competitive Analysis
17  Product Requirements Document
18  Implementation Roadmap
19  API Specification
20  Database Design
21  AI Model Document
22  Security Document
23  Testing Strategy
24  Prompt Engineering Guide
25  UI Component Library
26  Design Tokens
27  Acceptance Criteria
28  Hackathon MVP Scope
29  Demo Script (3-min)
30  Repository Standards
```
