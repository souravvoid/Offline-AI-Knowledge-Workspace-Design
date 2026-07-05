# Khoji Desktop

**Offline AI Knowledge Workspace** — PySide6 desktop application.

## Quick Start

```bash
cd khoji_desktop

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[ocr,dev]"

# Run
python -m khoji.main
```

## Architecture

```
src/khoji/
├── main.py                    # Entry point
├── database/
│   └── db.py                  # SQLite (documents, notes, flashcards, quiz, chat)
├── pipeline/
│   ├── pdf_extractor.py       # PyMuPDF text extraction
│   ├── ocr.py                 # RapidOCR / Tesseract fallback
│   ├── markdown_generator.py  # Structured markdown + chunking
│   ├── content_generator.py   # Flashcard & quiz generation
│   ├── processor.py           # QThread pipeline orchestrator
│   └── exporter.py            # Markdown, Anki, JSON, CSV export
├── ai/
│   ├── llm.py                 # llama.cpp local LLM (Qwen2.5/SmolLM2/TinyLlama)
│   ├── embeddings.py          # sentence-transformers (MiniLM-L6)
│   └── vector_search.py       # FAISS semantic search
├── ui/
│   ├── main_window.py         # QMainWindow with sidebar + stacked views
│   ├── theme.py               # Dark/light theme from design tokens
│   └── panels/
│       ├── library_panel.py   # Document grid, drag-drop upload
│       ├── notes_panel.py     # Markdown editor + preview
│       ├── flashcards_panel.py # Spaced repetition study
│       ├── quiz_panel.py      # Multiple choice quiz
│       ├── chat_panel.py      # AI chat with streaming
│       └── search_panel.py    # Semantic search across documents
└── utils/
```

## Features

| Feature | Status |
|---------|--------|
| PDF text extraction | ✅ PyMuPDF |
| OCR fallback | ✅ RapidOCR / Tesseract |
| Markdown generation | ✅ Template-based |
| Flashcards | ✅ Rule-based generation + spaced repetition |
| Quiz | ✅ Multiple choice from text |
| Local LLM | ✅ llama.cpp (auto-selects best model) |
| Semantic search | ✅ FAISS + sentence-transformers |
| AI Chat | ✅ Streaming responses |
| Export | ✅ Markdown, Anki, JSON, CSV |
| Dark/Light theme | ✅ Design tokens from spec |
| Drag & drop upload | ✅ |

## Database

SQLite at `~/.khoji/khoji.db` with tables:
- `documents` — metadata
- `document_chunks` — chunked text
- `notes` — markdown notes
- `flashcards` — spaced repetition cards
- `quiz_questions` — multiple choice
- `chat_sessions` / `chat_messages` — conversation history

## AI Models

Auto-selects best model based on available RAM:
- **Qwen2.5-1.5B** (high quality, ~1.2GB RAM)
- **SmolLM2-1.7B** (high quality, ~1.4GB RAM)
- **TinyLlama-1.1B** (medium quality, ~0.9GB RAM)

Models downloaded to `~/.khoji/models/` on first use.
