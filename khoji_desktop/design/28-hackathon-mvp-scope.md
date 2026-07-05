# Hackathon MVP Scope (3 Days)

## Scope Strategy

**Rule: If it doesn't directly demonstrate the core value proposition, cut it.**

Core value prop: "Upload a document → AI understands it locally → produces structured knowledge"

---

## P0 — Must Have (Ship without these = failure)

### Day 1: Foundation

| Feature | Effort | Why P0 |
|---------|--------|--------|
| Tauri + React + Tailwind project setup | 1hr | Foundation |
| App shell: TopBar + Sidebar + Main Area | 2hr | Navigation |
| Sidebar with navigation items | 1hr | Navigation |
| Library view (grid of document cards) | 3hr | Primary landing page |
| Upload zone (drag & drop + file picker) | 2hr | Document input |
| File type validation (PDF only for MVP) | 0.5hr | Safety |

### Day 2: Core Pipeline

| Feature | Effort | Why P0 |
|---------|--------|--------|
| PDF text extraction (pdf-extract Rust) | 3hr | Must parse PDFs |
| Basic OCR (Tesseract CLI) | 2hr | Scanned docs |
| Template-based Markdown generation | 3hr | Must produce output |
| Notes tab (rendered Markdown) | 2hr | Primary output |
| Export to Markdown file | 1hr | Must get data out |
| Processing pipeline UI (progress bar) | 2hr | User feedback |
| Dark mode toggle | 1hr | UX quality |

### Day 3: AI + Polish

| Feature | Effort | Why P0 |
|---------|--------|--------|
| Embedding generation (ONNX MiniLM) | 3hr | Semantic understanding |
| Semantic search (basic vector search) | 2hr | Must find information |
| AI Chat (prompt + stream response) | 4hr | Core interaction |
| Flashcard tab (basic card list) | 2hr | Knowledge output |
| Flashcard review mode (flip + rate) | 3hr | Study feature |
| Quiz tab (basic MCQ) | 3hr | Knowledge output |
| Simple pipeline progress visualization | 1hr | UX quality |
| Final integration + bug fixes | 2hr | Ship quality |

---

## P1 — Should Have (if time permits)

| Feature | Effort | Risk |
|---------|--------|------|
| Mermaid diagram generation | 3hr | Medium — LLM prompt tuning |
| Mind map tab with zoom/pan | 2hr | Low — UI only |
| Quiz full-screen mode with timer | 2hr | Low |
| Flashcard spaced repetition scheduling | 2hr | Medium — SM-2 algorithm |
| Export to Anki | 2hr | Medium — APKG format |
| Batch upload (multiple files) | 1hr | Low |
| Keyboard shortcuts | 2hr | Low |
| Processing queue | 2hr | Medium |
| Empty states | 1hr | Low |

---

## P2 — Nice to Have (demo only, not shipped)

| Feature | Effort | Why Not |
|---------|--------|---------|
| PPT/DOCX/EPUB support | 4hr+ | PDF is enough for demo |
| Knowledge graph | 6hr+ | Complex, post-MVP |
| AI memory | 4hr+ | Nice but not essential |
| Plugin system | 8hr+ | Full project, not hackathon |
| Git integration | 4hr+ | Post-MVP |
| Collections | 2hr | Nice but skippable |
| Settings (full) | 3hr | Minimal settings only |
| Mobile responsive | 3hr | Desktop only for hackathon |
| i18n | 4hr+ | English only for MVP |
| Image/vision understanding | 4hr+ | PDF text is enough for demo |
| LaTeX export | 2hr | Markdown export sufficient |
| Audio/podcast generation | — | Way out of scope |

---

## MVP Architecture (Simplified for Hackathon)

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                       │
│                                                          │
│  App Shell → Library → Upload → Process → Notes         │
│                                        → Flashcards      │
│                                        → Quiz            │
│                                        → Chat            │
│                                        → Export          │
└──────────────────────────┬──────────────────────────────┘
                           │ IPC
┌──────────────────────────┴──────────────────────────────┐
│                   BACKEND (Tauri/Rust)                    │
│                                                          │
│  Commands:                                               │
│    upload_document → parse_pdf → ocr → markdown          │
│    search → embed_query → cosine_similarity              │
│    chat → build_prompt → llama_inference → stream        │
│    export → write_file                                   │
│                                                          │
│  Models (downloaded once):                               │
│    Tesseract v5 (OCR)                                    │
│    all-MiniLM-L6-v2 (Embeddings)                         │
│    Llama 3.2 1B (LLM)                                    │
│                                                          │
│  Storage:                                                │
│    ~/.khoji/documents/                                   │
│    ~/.khoji/processed/                                   │
│    ~/.khoji/models/                                      │
│    ~/.khoji/config.json                                  │
└─────────────────────────────────────────────────────────┘
```

## Minimum Viable Demo Flow

```
1. Open Khoji → Library (empty state)
2. Click Upload → Select PDF
3. See pipeline processing (OCR → Embed → LLM)
4. Notes tab shows formatted Markdown
5. Flashcards tab shows auto-generated cards
6. Click "Review" → flip cards → rate them
7. Quiz tab shows MCQs → answer some
8. Chat: "Summarize chapter 1" → AI responds with citations
9. Search: type key term → results with highlights
10. Export: click Export → .md file saved
```

## MVP Tech Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Desktop framework | Tauri v2 | Small binary, Rust backend |
| Frontend | React + Vite | Fast setup, large ecosystem |
| Styling | Tailwind CSS | Rapid UI development |
| State | Zustand | Simple, no boilerplate |
| PDF parsing | pdf-extract (Rust) | Native performance |
| OCR | Tesseract CLI | Easy to integrate |
| Embeddings | ONNX Runtime + MiniLM | Small, fast, CPU-friendly |
| Vector search | In-memory FAISS | Simple, no DB setup |
| LLM | llama.cpp + Llama 3.2 1B | Best quality/speed for 4GB |
| Markdown | react-markdown | Renders Markdown natively |
| Icons | Lucide React | Consistent, easy |
| Storage | Simple JSON files | No database setup needed |

## What to Pre-Download Before Hackathon

| Item | Size | Purpose |
|------|------|---------|
| Tauri CLI + Rust toolchain | 2GB | Build system |
| Node.js + npm packages | 500MB | Frontend |
| Tesseract v5 binary + English data | 50MB | OCR |
| all-MiniLM-L6-v2 ONNX model | 80MB | Embeddings |
| Llama 3.2 1B Q4_K_M GGUF | 620MB | LLM |
| Sample PDFs (clean + scanned) | 10MB | Testing |
| Total | ~3.3GB | |

## Team Role Assignment (4-person team)

| Person | Focus | Day 1 | Day 2 | Day 3 |
|--------|-------|-------|-------|-------|
| **A** | Frontend Lead | App shell, Sidebar, Library view | Notes tab, Chat UI, Flashcard UI | Quiz UI, Polish, Dark mode |
| **B** | Backend Lead | PDF parsing, OCR integration | LLM integration, Embeddings | Search, Export, Bug fixes |
| **C** | Fullstack | Upload zone, Processing UI | Flashcard gen, Quiz gen prompts | Integration testing, Demo prep |
| **D** | Design + PM | Design tokens, Component polish | Chat prompt design, Error states | Demo script, Presentation |

## What the Judges Will See (3-min Demo)

```
0:00 - Problem: Knowledge is fragmented across tools
0:15 - Solution: Khoji — upload any document, get everything
0:30 - Live: Upload PDF → watch AI pipeline
1:00 - Live: Browse auto-generated notes
1:15 - Live: Review flashcards with flip animation
1:30 - Live: Take quiz, see smart questions
1:45 - Live: Chat with AI about document
2:00 - Live: Semantic search finds exact answer
2:15 - Architecture: All local, multi-agent AI
2:30 - Roadmap: What's next (graph, plugins, mobile)
2:45 - Q&A
```
