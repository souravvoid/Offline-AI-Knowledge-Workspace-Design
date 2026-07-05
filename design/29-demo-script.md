# Demo Script (3-Minute Presentation)

**Format:** Live demo on projector (1080p), single presenter with hot mic.

---

## Slide 0: Title Card (15 seconds)

| Visual | Script |
|--------|--------|
| Logo + "Khoji" + tagline: "Your Offline AI Knowledge OS" | "Meet Khoji — an open-source, offline AI knowledge operating system that turns any document into structured, connected knowledge. Entirely local. Entirely private." |

---

## Slide 1: The Problem (15 seconds)

| Visual | Script |
|--------|--------|
| Split screen: Student with 5 tabs (PDF, Obsidian, Anki, ChatGPT, Browser) vs Khoji one-screen | "Students and researchers use 5 different tools to read a single PDF — reading, note-taking, flashcards, searching, and chatting. Nothing connects. Nothing remembers. And none of it works offline." |

---

## Slide 2: The Solution (15 seconds)

| Visual | Script |
|--------|--------|
| Animated: Document → AI pipeline → Notes + Flashcards + Quiz + Chat | "Khoji is one tool that does it all. Upload any document — PDF, image, PPT, DOCX, EPUB — and specialized AI agents extract, organize, and connect the knowledge for you. All running locally on your machine." |

---

## Live Demo: Upload & Process (30 seconds)

| Visual | Script |
|--------|--------|
| Screen opens to empty library. Drag a PDF onto upload zone. Pipeline appears. | "Let me show you. I'll drag in a quantum mechanics textbook — 240 pages. One click to process. Watch the AI pipeline..." |
| Pipeline stages light up one by one: OCR → Layout → Chunking → Embeddings → LLM → Flashcards → Quiz → Diagrams | "The OCR agent extracts text. The layout agent understands structure. A specialized LLM generates notes, flashcards, and diagrams. Every agent is purpose-built for its job." |

---

## Live Demo: Notes & Flashcards (30 seconds)

| Visual | Script |
|--------|--------|
| Pipeline completes. Click Notes tab. Scroll through formatted Markdown. | "And here are the results. Beautifully structured Markdown notes with definitions, formulas rendered in LaTeX, and Mermaid diagrams — all generated automatically." |
| Switch to Flashcards tab. Click "Review." Flip a card. Rate it "Good." | "20 flashcards, generated from the document. Let me review one. Tap to flip. Rate how well I knew it. Spaced repetition schedules the next review at the optimal time." |

---

## Live Demo: Quiz & Chat (30 seconds)

| Visual | Script |
|--------|--------|
| Switch to Quiz tab. Click "Start Quiz." Answer 2 questions. | "10 quiz questions across difficulty levels. I'll answer a couple — instant feedback with explanations citing the source page." |
| Open chat panel. Type: "Explain the double-slit experiment in simple terms." Watch streaming response with citations. | "The AI chat knows which document I'm looking at. I can ask questions, request explanations, or generate more content using slash commands." |

---

## Live Demo: Search (15 seconds)

| Visual | Script |
|--------|--------|
| Press Cmd+K. Type "wave function." Results appear with snippets and scores. | "Semantic search across all documents. I type 'wave function' and it finds the exact passage across my entire library, ranked by relevance. All powered by local vector embeddings." |

---

## Slide 3: Architecture (15 seconds)

| Visual | Script |
|--------|--------|
| Simple arch diagram: React Frontend ↔ Tauri IPC ↔ Rust Backend ↔ AI Models | "The architecture: React frontend, Rust backend via Tauri, all AI models run locally. Tesseract for OCR, ONNX for embeddings, llama.cpp for the language model. Every model runs on-device — nothing leaves your computer." |

---

## Slide 4: Key Differentiators (15 seconds)

| Visual | Script |
|--------|--------|
| Comparison table: Khoji vs NotebookLM vs Obsidian vs ChatGPT | "Unlike NotebookLM, we're fully offline. Unlike Obsidian, we have built-in AI that understands documents. Unlike ChatGPT, we're private and free. And unlike all of them, we produce flashcards, quizzes, mind maps, and knowledge graphs from every document." |

---

## Slide 5: Roadmap (10 seconds)

| Visual | Script |
|--------|--------|
| Roadmap: Knowledge Graph → Plugin SDK → Mobile → Tutoring | "Over the next year: interactive knowledge graphs that connect concepts across all your documents, a plugin SDK for community extensions, mobile companion for review on the go, and AI tutoring that adapts to your learning." |

---

## Closing (10 seconds)

| Visual | Script |
|--------|--------|
| Logo + GitHub QR code + "Star us on GitHub" | "Khoji is open source. Star us on GitHub, contribute a plugin, or just download it and try it yourself. Your knowledge belongs to you — offline, private, and beautifully organized." |

---

## Total: 3 minutes 0 seconds

---

## Backup Plan (if demo fails)

| Failure | Recovery |
|---------|----------|
| AI model too slow | Pre-recorded video of pipeline running on faster machine |
| Tauri build failure | React dev server with mock backend |
| LLM crashes | Fallback to template-generated content |
| OCR fails on demo PDF | Have 3 backup PDFs ready (clean + scanned + image) |
| No projector port | Run on presenter's laptop, crowd around; or screen share via Zoom |
| Audio issues | Text overlay on slides; presenter speaks louder |
| Internet down | Everything already downloaded; run fully offline |

## Technical Setup Checklist

```
□ Laptop fully charged
□ External monitor/projector cable
□ PDF files downloaded (clean, scanned, image-based)
□ All models pre-downloaded (Tesseract, MiniLM, Llama)
□ App running in production mode (not dev server)
□ Terminal closed (no code visible)
□ Dark mode activated (better projection contrast)
□ Font size at 120% for visibility
□ Sound check (notification sounds off)
□ Backup video recording ready
□ GitHub repo open on QR code slide
□ USB-C to HDMI adapter
```

## What Judges Look For

| Criteria | How We Score |
|----------|-------------|
| **Technical complexity** | Multi-agent AI pipeline, local LLM, 2+ model types |
| **User experience** | Smooth pipeline visualization, flashcard flip, streaming chat |
| **Open source** | AGPL license, CONTRIBUTING.md, plugin SDK planned |
| **Completeness** | Upload → process → view → chat → export in one flow |
| **Offline capability** | No network calls during demo, models pre-loaded |
| **Innovation** | Knowledge graph + AI memory + multi-agent architecture |
| **Design quality** | Consistent design system, dark mode, responsive |
