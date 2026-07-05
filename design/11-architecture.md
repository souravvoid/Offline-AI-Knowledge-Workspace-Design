# Phase 17: Architecture Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         KHOJI ARCHITECTURE                              │
│                    Offline AI Knowledge Workspace                        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Desktop App)                          │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     UI Layer (React/Preact)                      │    │
│  │                                                                  │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐    │    │
│  │  │ Library  │ │Document  │ │ Chat     │ │ Markdown Preview │    │    │
│  │  │ View     │ │Workspace │ │ Panel    │ │ + Editor         │    │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘    │    │
│  │                                                                  │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐    │    │
│  │  │Flashcards│ │Quiz      │ │Mind Map  │ │ Settings /       │    │    │
│  │  │ Review   │ │Engine    │ │Renderer  │ │ Model Manager    │    │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘    │    │
│  │                                                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                   State Management (Zustand)                     │    │
│  │                                                                  │    │
│  │  store = {                                                       │    │
│  │    documents: Map<id, Document>,                                 │    │
│  │    collections: Map<id, Collection>,                             │    │
│  │    activeDocument: string | null,                                │    │
│  │    activeTab: TabType,                                           │    │
│  │    ui: { sidebarOpen, chatOpen, theme, ... },                    │    │
│  │    processing: ProcessingState[],                                │    │
│  │    review: { queue, stats, ... },                                │    │
│  │    chat: { sessions: Map<id, Message[]>, ... }                   │    │
│  │  }                                                               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     IPC Bridge (Tauri Commands)                  │    │
│  │                                                                  │    │
│  │  invoke('process_document', { path })        → ProcessingResult  │    │
│  │  invoke('search_documents', { query })        → SearchResult[]    │    │
│  │  invoke('ask_ai', { docId, message })         → Stream<String>    │    │
│  │  invoke('generate_flashcards', { docId })     → Flashcard[]       │    │
│  │  invoke('export_document', { docId, format }) → FilePath          │    │
│  │  invoke('get_models', {})                      → ModelInfo[]       │    │
│  │  invoke('download_model', { modelId })        → Progress          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                    │
└────────────────────────────────────┼────────────────────────────────────┘
                                     │ IPC (JSON-RPC over WebSocket/Stdio)
┌────────────────────────────────────┼────────────────────────────────────┐
│                         BACKEND (Rust/Tauri Core)                      │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     Orchestrator Service                         │    │
│  │                                                                  │    │
│  │  • Manages document processing pipeline                          │    │
│  │  • Coordinates dispatching to worker threads                     │    │
│  │  • Tracks processing progress and state                          │    │
│  │  • Handles cancellation and error recovery                       │    │
│  │  • Manages model lifecycle (load/unload)                         │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    Document Processing Pipeline                   │    │
│  │                                                                  │    │
│  │  Input → [Parser] → [OCR] → [Layout Analysis] → [Chunker]       │    │
│  │            ↓                                                     │    │
│  │          [Embedder] → [(Vector DB)]                              │    │
│  │            ↓                                                     │    │
│  │          [LLM Processor] → [Notes] → [Flashcards]               │    │
│  │                            → [Quiz] → [Mind Map]                │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                    │
│  ┌────────────┬────────────┬───────────────┬─────────────┬───────────┐  │
│  │   Parser   │   OCR      │   Embedder    │    LLM      │ Vector DB │  │
│  │  Module    │  Module    │   Module      │   Module    │  Module   │  │
│  ├────────────┼────────────┼───────────────┼─────────────┼───────────┤  │
│  │ PDF:       │ Tesseract  │ Sentence-     │ llama.cpp   │ SQLite    │  │
│  │ pdf-extract│ EasyOCR    │ Transformers  │ onnx-runtime│ +         │  │
│  │ PPT:       │ Surya OCR  │ All-MiniLM    │ llama-      │ vec-      │  │
│  │ python-pptx│            │               │ rs         │ quantized │  │
│  │ DOCX:      │            │               │             │           │  │
│  │ docx-rs    │            │               │             │           │  │
│  │ EPUB:      │            │               │             │           │  │
│  │ epub-rs    │            │               │             │           │  │
│  └────────────┴────────────┴───────────────┴─────────────┴───────────┘  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     File System Layer                             │    │
│  │                                                                  │    │
│  │  ~/.khoji/                                                       │    │
│  │    ├── documents/         # Original uploaded files               │    │
│  │    ├── processed/         # Generated notes, md files             │    │
│  │    ├── models/            # Downloaded AI models                  │    │
│  │    ├── db/                # SQLite databases                      │    │
│  │    │   ├── khoji.db       # Main app database                    │    │
│  │    │   └── vectors.db     # Vector embeddings database           │    │
│  │    ├── cache/             # Rendered diagrams, thumbnails        │    │
│  │    └── config.json        # User preferences                     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Diagram

```
┌────────────────────────────┐
│       App Shell            │
│  ┌──────────────────────┐  │
│  │      TopBar          │  │
│  ├─────────┬────────────┤  │
│  │ Sidebar │  Main Area │  │
│  │         │            │  │
│  │  Nav    │ ┌────────┐ │  │
│  │  Items  │ │ Content│ │  │
│  │         │ │ Area   │ │  │
│  │ Library │ └────────┘ │  │
│  │ Notes   │            │  │
│  │ Cards   │ ┌────────┐ │  │
│  │ Quiz    │ │ Chat   │ │  │
│  │ Chat    │ │ Panel  │ │  │
│  │ Search  │ └────────┘ │  │
│  │ Settings│            │  │
│  └─────────┴────────────┘  │
│  ┌──────────────────────┐  │
│  │    StatusBar         │  │
│  └──────────────────────┘  │
└────────────────────────────┘

Key Components:
  • AppShell          — Root layout, sidebar/topbar/statusbar
  • Sidebar           — Navigation, collapsible
  • TopBar            — Search (Cmd+K), upload, user menu
  • LibraryView       — Document grid/list, collections
  • UploadZone        — Drag & drop, file selection
  • ProcessingModal   — Pipeline progress visualization
  • DocumentWorkspace — Tab container for document views
  • NotesTab          — Markdown rendered notes
  • FlashcardsTab     — Card list + review mode
  • QuizTab           — Quiz engine + fullscreen mode
  • MindMapTab        — Interactive Mermaid diagram
  • TimelineTab       — Chronological event view
  • ChatPanel         — AI chat with document context
  • SearchModal       — Global semantic search (Cmd+K)
  • SettingsDrawer    — All settings organized by section
  • ModelManager      — Download/select AI models
  • ExportDialog      — Format selection + options
  • EmptyState        — Contextual empty states
  • ErrorBoundary     — Crash recovery with feedback
```

## Data Flow Diagram

```
┌──────────┐    Upload    ┌───────────┐    File Path    ┌──────────┐
│  User    │ ────────────▶│  Frontend │ ───────────────▶│  Backend │
│  (UI)    │              │  (React)  │                  │  (Rust)  │
│          │◄─────────────│           │◄─────────────────│          │
└──────────┘    Result     └───────────┘    Response      └──────────┘
                              │    ▲                        │    ▲
                              │    │                        │    │
                         Events │    │ Queries          Events │    │ IPC
                              │    │                        │    │
                              ▼    │                        ▼    │
                          ┌──────────┐                  ┌──────────┐
                          │  State   │                  │  Worker  │
                          │  Store   │                  │  Pool    │
                          │(Zustand) │                  │(Threads) │
                          └──────────┘                  └──────────┘

Search Flow:
  User types query → Debounce 300ms → IPC invoke('search')
  → Embed query → Cosine similarity against vector DB
  → Rank results → Return to UI → Render with highlights

Chat Flow:
  User sends message → IPC invoke('ask_ai')
  → Build prompt (system + document context + query)
  → LLM inference → Stream tokens → UI renders progressively
  → Save to chat history

Export Flow:
  User selects format → IPC invoke('export')
  → Read processed markdown → Convert to target format
  → Write to user's chosen directory → Return path
  → Show success notification
```

## State Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                          APPLICATION STATES                           │
│                                                                       │
│                    ┌──────────┐                                       │
│                    │  Launch  │                                       │
│                    └────┬─────┘                                       │
│                         │                                             │
│                    ┌────▼─────┐                                       │
│         ┌─────────│ First Run│──────────┐                             │
│         │         └────┬─────┘          │                             │
│         │              │                │                             │
│         ▼              ▼                ▼                             │
│  ┌──────────┐   ┌───────────┐   ┌──────────────┐                     │
│  │  Setup   │   │  Library  │   │ Import From   │                     │
│  │  Wizard  │──▶│  (Ready)  │──▶│ Previous Ver   │                     │
│  └──────────┘   └─────┬─────┘   └──────────────┘                     │
│                       │                                               │
│         ┌─────────────┼─────────────┐                                │
│         ▼             ▼             ▼                                │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐                          │
│  │  Upload   │ │  Search   │ │  Settings │                          │
│  └─────┬─────┘ └───────────┘ └───────────┘                          │
│        │                                                             │
│        ▼                                                             │
│  ┌───────────┐                                                       │
│  │Processing │───┐                                                   │
│  └─────┬─────┘   │  ┌──────────┐                                    │
│        │         ├──│  Failed  │──────────────────┐                  │
│   ┌────▼────┐    │  └──────────┘                  │                  │
│   │ Complete │◄──┘                                │                  │
│   └────┬────┘                                     │                  │
│        │                                          │                  │
│   ┌────▼────┐                                     │                  │
│   │Document │                                     │                  │
│   │Workspace│──┬───────────────────────────────────┤                  │
│   └────┬────┘  │                                   │                  │
│        │       │                                   │                  │
│   ┌────┴───┐   │  ┌───────────┐  ┌─────────┐     │                  │
│   │  View  │   ├──│  Review   │  │  Chat   │     │                  │
│   │  Notes │   │  │Flashcards │  │  Panel  │     │                  │
│   └────────┘   │  └───────────┘  └─────────┘     │                  │
│                │                                  │                  │
│   ┌────────┐   │  ┌──────────┐  ┌────────────┐   │                  │
│   │  Take  │   ├──│  Export  │  │  Generate   │   │                  │
│   │  Quiz  │   │  │  Dialog  │  │  Mind Map   │   │                  │
│   └────────┘   │  └──────────┘  └────────────┘   │                  │
│                │                                  │                  │
│                └──────────────────────────────────┘                  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Sequence Diagram: Document Processing

```
User         Frontend           Orchestrator        Parser/OCR      LLM         VectorDB
 │              │                    │                  │             │            │
 │  Upload PDF  │                    │                  │             │            │
 │─────────────▶│                    │                  │             │            │
 │              │  invoke('process') │                  │             │            │
 │              │───────────────────▶│                  │             │            │
 │              │                    │  parse_pdf()     │             │            │
 │              │                    │─────────────────▶│             │            │
 │              │                    │                  │             │            │
 │              │                    │  ←── text ───────│             │            │
 │              │                    │                  │             │            │
 │              │                    │  ocr_images()    │             │            │
 │              │                    │─────────────────▶│             │            │
 │              │    progress: 25%   │                  │             │            │
 │              │◄───────────────────│                  │             │            │
 │              │                    │  ←── ocr_text ───│             │            │
 │              │                    │                  │             │            │
 │              │                    │  embed_text()    │             │            │
 │              │    progress: 50%   │───────────────────────────────────────────▶│
 │              │◄───────────────────│                  │             │            │
 │              │                    │                  │             │            │
 │              │                    │  llm_process()   │             │            │
 │              │    progress: 75%   │──────────────────────────────▶│            │
 │              │◄───────────────────│                  │             │            │
 │              │                    │                  │             │            │
 │              │                    │  ←── notes ──────│─────────────│            │
 │              │                    │  ←── flashcards ─│─────────────│            │
 │              │                    │  ←── quiz ───────│─────────────│            │
 │              │                    │  ←── mindmap ────│─────────────│            │
 │              │                    │                  │             │            │
 │              │  result: complete  │                  │             │            │
 │              │◄───────────────────│                  │             │            │
 │              │                    │                  │             │            │
 │   Show       │                    │                  │             │            │
 │  Workspace   │                    │                  │             │            │
 │◄─────────────│                    │                  │             │            │
```

## Folder Structure

```
khoji/
├── src/
│   ├── frontend/                    # UI Application
│   │   ├── components/             # Reusable components
│   │   │   ├── ui/                 # Design system primitives
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Tabs.tsx
│   │   │   │   ├── Badge.tsx
│   │   │   │   ├── Tooltip.tsx
│   │   │   │   ├── Spinner.tsx
│   │   │   │   ├── ProgressBar.tsx
│   │   │   │   └── Dropdown.tsx
│   │   │   ├── layout/
│   │   │   │   ├── AppShell.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── TopBar.tsx
│   │   │   │   └── StatusBar.tsx
│   │   │   ├── library/
│   │   │   │   ├── LibraryView.tsx
│   │   │   │   ├── DocumentCard.tsx
│   │   │   │   ├── UploadZone.tsx
│   │   │   │   └── CollectionList.tsx
│   │   │   ├── document/
│   │   │   │   ├── DocumentWorkspace.tsx
│   │   │   │   ├── NotesTab.tsx
│   │   │   │   ├── FlashcardsTab.tsx
│   │   │   │   ├── QuizTab.tsx
│   │   │   │   ├── MindMapTab.tsx
│   │   │   │   ├── TimelineTab.tsx
│   │   │   │   └── OutlinePanel.tsx
│   │   │   ├── chat/
│   │   │   │   ├── ChatPanel.tsx
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   └── ChatInput.tsx
│   │   │   ├── search/
│   │   │   │   ├── SearchModal.tsx
│   │   │   │   └── SearchResult.tsx
│   │   │   ├── review/
│   │   │   │   ├── FlashcardReview.tsx
│   │   │   │   └── ReviewStats.tsx
│   │   │   ├── settings/
│   │   │   │   ├── SettingsDrawer.tsx
│   │   │   │   ├── ModelManager.tsx
│   │   │   │   └── ExportDialog.tsx
│   │   │   ├── processing/
│   │   │   │   ├── ProcessingModal.tsx
│   │   │   │   └── PipelineVisualization.tsx
│   │   │   └── empty-states/
│   │   │       ├── EmptyLibrary.tsx
│   │   │       ├── EmptyNotes.tsx
│   │   │       ├── EmptyFlashcards.tsx
│   │   │       ├── EmptyQuiz.tsx
│   │   │       ├── EmptyMindMap.tsx
│   │   │       ├── EmptySearch.tsx
│   │   │       └── EmptyChat.tsx
│   │   ├── hooks/                  # Custom React hooks
│   │   │   ├── useDocuments.ts
│   │   │   ├── useSearch.ts
│   │   │   ├── useChat.ts
│   │   │   ├── useProcessing.ts
│   │   │   ├── useReview.ts
│   │   │   └── useKeyboard.ts
│   │   ├── stores/                 # State management
│   │   │   ├── documentStore.ts
│   │   │   ├── uiStore.ts
│   │   │   ├── chatStore.ts
│   │   │   ├── reviewStore.ts
│   │   │   └── settingsStore.ts
│   │   ├── lib/                    # Utilities
│   │   │   ├── ipc.ts             # Tauri invoke wrapper
│   │   │   ├── markdown.ts        # Markdown rendering
│   │   │   ├── mermaid.ts         # Mermaid renderer
│   │   │   ├── keyboard.ts        # Keyboard shortcuts
│   │   │   ├── format.ts          # Formatting utils
│   │   │   └── constants.ts       # App constants
│   │   ├── styles/                 # CSS, design tokens
│   │   │   ├── tokens.css
│   │   │   ├── global.css
│   │   │   ├── light.css
│   │   │   └── dark.css
│   │   └── App.tsx                 # Root component
│   │
│   └── backend/                    # Rust/Tauri Core
│       ├── src/
│       │   ├── main.rs            # Entry point
│       │   ├── commands/          # IPC command handlers
│       │   │   ├── mod.rs
│       │   │   ├── document.rs
│       │   │   ├── search.rs
│       │   │   ├── chat.rs
│       │   │   ├── flashcard.rs
│       │   │   ├── quiz.rs
│       │   │   ├── export.rs
│       │   │   └── models.rs
│       │   ├── pipeline/          # Document processing
│       │   │   ├── mod.rs
│       │   │   ├── orchestrator.rs
│       │   │   ├── parser.rs
│       │   │   ├── ocr.rs
│       │   │   ├── chunker.rs
│       │   │   ├── embedder.rs
│       │   │   └── llm.rs
│       │   ├── db/                # Database
│       │   │   ├── mod.rs
│       │   │   ├── schema.rs
│       │   │   ├── documents.rs
│       │   │   ├── vectors.rs
│       │   │   └── migrations.rs
│       │   ├── models/            # AI model interfaces
│       │   │   ├── mod.rs
│       │   │   ├── ocr.rs
│       │   │   ├── embedding.rs
│       │   │   └── llm.rs
│       │   ├── export/            # Export formats
│       │   │   ├── mod.rs
│       │   │   ├── markdown.rs
│       │   │   ├── anki.rs
│       │   │   ├── pdf.rs
│       │   │   └── latex.rs
│       │   └── utils/             # Shared utilities
│       │       ├── mod.rs
│       │       ├── file.rs
│       │       ├── config.rs
│       │       └── logging.rs
│       ├── Cargo.toml
│       └── build.rs
│
├── models/                        # AI model storage (gitignored)
├── tests/                         # Test files
├── docs/                          # Documentation
├── scripts/                       # Build/dev scripts
├── .github/                       # CI/CD
├── package.json
├── tauri.conf.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.ts
└── README.md
```
