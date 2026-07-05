# Khoji MVP — Completed

## Day 1: Scaffold & Library View
- **Tauri v2 + React + Vite + TailwindCSS** project scaffolded
- **AppShell** — sidebar document list + main content area
- **File upload** via `tauri-plugin-dialog`
- **Document Library** — list documents, status badges, delete
- **Zustand stores**: documentStore, uiStore, chatStore, reviewStore, settingsStore

## Day 2: Processing Pipeline & Notes
- **PDF text extraction** (`pdf-extract` crate, pure Rust)
- **Tesseract OCR fallback** for scanned images
- **5-stage pipeline**: PDF parse → layout → markdown → flashcards → quiz
- **Real-time progress events** via Tauri event system
- **Notes tab** — Markdown rendering + inline editing
- **Export** (Markdown/JSON to file)
- **`storage.rs`** — JSON file-based persistence (metadata, raw text, notes, flashcards, quiz, chat)

## Day 3: Flashcards, Quiz, Chat, Search
- **Flashcard generation** (~25 cards per doc) from definition patterns
- **Spaced repetition review** with 4-level rating (Again/Hard/Good/Easy)
- **Quiz generation** (~10 MCQs) with distractors from document text
- **Quiz session flow** — progress bar, answer checking, explanations, score
- **Chat backend** — query routing (summarize, flashcard, quiz, search, fallback QA with keyword matching)
- **Streaming chat** via Tauri events (`chat:token`/`chat:complete`) with typewriter UI
- **Semantic-ish search** across all documents with relevance scoring
- **All 12 IPC commands** registered in `lib.rs`

## Build Status
- `cargo build` — 0 errors, 0 warnings
- `npx tsc --noEmit` — 0 errors
- `npx @tauri-apps/cli dev` — launches successfully

## Key Files
| File | Purpose |
|------|---------|
| `src-tauri/src/commands.rs` | 12 IPC command handlers + `chat_ask` streaming |
| `src-tauri/src/pipeline.rs` | 5-stage processing pipeline |
| `src-tauri/src/storage.rs` | File-based persistence layer |
| `src/App.tsx` | Main app layout + routing |
| `src/components/notes/NotesView.tsx` | Markdown notes viewer/editor |
| `src/components/flashcards/FlashcardsView.tsx` | Flashcard list + review mode |
| `src/components/quiz/QuizView.tsx` | Quiz session with scoring |
| `src/components/chat/ChatView.tsx` | Streaming chat interface |
| `src/components/search/SearchView.tsx` | Cross-document search |
| `src/lib/ipc.ts` | Frontend IPC wrapper + event listeners |
