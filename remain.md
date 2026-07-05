# Khoji — Remaining Work

## P0 — Real AI Model Integration (blocked without model downloads)

### 1. ONNX Embeddings + Vector Search
- **Files to create:**
  - `src-tauri/src/models/embedding.rs` — ONNX Runtime session for all-MiniLM-L6-v2
  - `src-tauri/src/pipeline/embedder.rs` — chunk → embedding pipeline
  - `src-tauri/src/pipeline/searcher.rs` — cosine similarity search
- **Dependencies:** `ort` (ONNX Runtime crate)
- **Model:** `all-MiniLM-L6-v2.onnx` (~80MB) — download to `~/.khoji/models/`
- **Integration points:**
  - `commands.rs` `search_documents` — replace keyword BM25 with cosine similarity
  - `pipeline.rs` `process_document` — add embedding step after text extraction
  - Store vectors alongside chunks in `storage.rs` or a `vectors.db` (sqlite-vec)
- **Verification:** Search returns semantically relevant results (e.g., "car" matches "vehicle")

### 2. llama.cpp LLM Integration
- **Files to create:**
  - `src-tauri/src/models/llm.rs` — llama.cpp subprocess or `llama-cpp-2` crate binding
  - Prompt templates in `src-tauri/src/pipeline/prompts.rs`
- **Dependencies:** `llama-cpp-2` crate or direct subprocess to `llama-server`
- **Model:** `Llama-3.2-1B-Q4_K_M.gguf` (~620MB) — download to `~/.khoji/models/`
- **Integration points:**
  - `commands.rs` `chat_ask` — replace template-based responses with real LLM inference
  - `pipeline.rs` — replace flashcard/quiz template generation with LLM calls
  - Add a `models.rs` module to manage model loading/unloading
- **Verification:** Chat returns coherent, document-grounded answers

### 3. Model Download Manager
- **File:** `src-tauri/src/commands.rs` — `download_model` / `get_models` commands
- **UI:** Model management panel in settings
- **Verification:** SHA256 verification of downloaded models

---

## P1 — Should Have (time-permitting enhancements)

### 4. Knowledge Graph
- **Rust:** Command to extract concepts + relationships from text (`concepts.rs`)
- **Storage:** `concepts.json`, `concept_relationships.json` per document
- **UI:** Force-directed graph component (D3.js or vis.js)
- **Integration:** Click concept node → show related notes/flashcards

### 5. Mind Map
- **UI only:** Interactive Mermaid diagram with zoom/pan
- **Backend:** Generate Mermaid markdown from document outline
- **Tab:** Add to tab list in `App.tsx`

### 6. Quiz Full-Screen Mode + Timer
- **UI feature in QuizView:** Full-screen button, countdown timer per question
- **Results:** Time taken per question, accuracy vs speed stats

### 7. Flashcard Spaced Repetition (SM-2)
- **Rust:** Implement SM-2 algorithm in `storage.rs` review calculation
- **ReviewQueue:** Smart ordering by due date + ease factor
- **Stats:** Cards due today, retention rate, reviews per day

### 8. Anki Export
- **Rust:** Generate `.apkg` file (SQLite + media zip)
- **UI:** Add "Export to Anki" button in flashcards tab
- **Verification:** Import into Anki desktop

### 9. Batch Upload
- **UI:** Multi-file selection in dialog
- **Backend:** Processing queue with concurrent limit

### 10. Processing Queue
- **Rust:** `processing_queue` in storage, sequential processing
- **UI:** Queue status indicator in sidebar

### 11. Keyboard Shortcuts
- `Cmd+K` — Search
- `Cmd+U` — Upload
- `Cmd+1-4` — Switch tabs
- `Cmd+B` — Toggle sidebar
- `Space` — Flip flashcard
- `1-4` — Rate flashcard

### 12. Empty & Error States
- **Components needed:** `EmptyState.tsx`, `ErrorBoundary.tsx`, `ErrorFallback.tsx`
- **Every view:** Loading, empty, error, and edge case states

---

## P2 — Nice to Have (post-MVP)

### 13. Additional Document Formats
- PPT/DOCX/EPUB parsing (add crates for each)
- Unified document trait in Rust

### 14. AI Memory System
- User corrections persisted and applied to future processing
- `ai_memory.json`, `ai_corrections.json` in storage

### 15. Plugin System (WASM)
- Plugin SDK with WASM sandbox (wasmtime)
- Plugin registry UI
- Marketplace API

### 16. Settings Page
- Model configuration (which models to use)
- Export defaults
- Theme customization
- Storage path config

### 17. Collections / Document Groups
- Tag-based or folder-based document organization
- Cross-document search within collection

### 18. Testing (all types)
- **Unit tests:** All Rust functions, React components
- **Integration:** IPC commands end-to-end
- **E2E:** Playwright for critical user flows
- **Target:** 80%+ coverage

### 19. CI/CD
- GitHub Actions: lint, typecheck, test, build
- Pre-commit hooks

### 20. Documentation
- User docs (how to use each feature)
- Developer docs (architecture, contributing)
- API docs (IPC command reference)

---

## Current Implementation Summary

| Area | What's Done | What's Template/Placeholder |
|------|------------|---------------------------|
| PDF parsing | `pdf-extract` + Tesseract OCR | — |
| Markdown notes | Template-based generation + edit UI | — |
| Flashcards | Template generation + full UI (list, flip, rate) | Not LLM-generated |
| Quiz | Template generation + full UI (session, score) | Not LLM-generated |
| Chat | Streaming UI with template responses | Not real LLM |
| Search | Keyword BM25 + UI | Not semantic/vector |
| Export | Markdown file export | No Anki/PDF/LaTeX |
| Dark mode | Toggle + CSS vars | — |
| Storage | JSON file-based | No vector DB, no SQLite |
