# API Specification (Tauri IPC Commands)

Khoji uses **Tauri Commands** (JSON-RPC over IPC) for all frontend-backend communication. Since this is a desktop app, there is no REST/HTTP API — all calls are local function invocations.

---

## Command: `upload_document`

**Description:** Upload a document file for processing

```
invoke('upload_document', { path: '/home/user/doc.pdf' })
```

**Request:**
```json
{
  "path": "/absolute/path/to/file.pdf",
  "collection_id": "optional-collection-id"
}
```

**Response (success):**
```json
{
  "document_id": "doc-uuid-1234",
  "title": "Quantum Mechanics",
  "file_type": "pdf",
  "file_size_bytes": 24500000,
  "page_count": 240,
  "status": "uploaded",
  "created_at": "2026-07-03T10:30:00Z"
}
```

**Errors:**
| Code | Message | Cause |
|------|---------|-------|
| `FILE_NOT_FOUND` | File does not exist at path | Invalid path |
| `UNSUPPORTED_FORMAT` | Format .xyz not supported | Not in [pdf, png, jpg, ppt, pptx, doc, docx, epub] |
| `FILE_TOO_LARGE` | File exceeds 200MB limit | Size check |
| `STORAGE_FULL` | Disk quota exceeded | Storage policy |
| `DUPLICATE` | Document already exists | Same filename + size |

---

## Command: `process_document`

**Description:** Start AI processing pipeline on an uploaded document

```
invoke('process_document', { document_id: 'doc-uuid-1234', model_config: {...} })
```

**Request:**
```json
{
  "document_id": "doc-uuid-1234",
  "model_config": {
    "ocr": "tesseract-v5",
    "embedding": "all-minilm-l6-v2",
    "llm": "llama-3.2-1b",
    "generate_flashcards": true,
    "generate_quiz": true,
    "generate_diagrams": true,
    "generate_timeline": false
  }
}
```

**Response:**
```json
{
  "job_id": "job-uuid-5678",
  "status": "queued",
  "estimated_seconds": 75
}
```

**Progress Updates (via event):**
```json
{
  "event": "processing:progress",
  "data": {
    "job_id": "job-uuid-5678",
    "stage": "llm_processing",
    "stage_index": 3,
    "total_stages": 8,
    "progress_pct": 0.65,
    "message": "AI analyzing document structure...",
    "sub_steps": [
      {"label": "PDF parsing", "status": "completed"},
      {"label": "OCR & layout", "status": "completed"},
      {"label": "Text chunking", "status": "completed"},
      {"label": "Embeddings", "status": "completed"},
      {"label": "LLM processing", "status": "active"},
      {"label": "Flashcard gen", "status": "pending"},
      {"label": "Quiz gen", "status": "pending"},
      {"label": "Diagram gen", "status": "pending"}
    ]
  }
}
```

**Completion Event:**
```json
{
  "event": "processing:complete",
  "data": {
    "job_id": "job-uuid-5678",
    "document_id": "doc-uuid-1234",
    "duration_seconds": 82,
    "results": {
      "notes_paragraphs": 145,
      "flashcards_generated": 22,
      "quiz_questions": 10,
      "diagrams_generated": 3
    }
  }
}
```

**Error Event:**
```json
{
  "event": "processing:error",
  "data": {
    "job_id": "job-uuid-5678",
    "stage": "ocr",
    "error_code": "OCR_FAILED",
    "message": "Could not extract text from images. Try a higher quality scan.",
    "suggestions": ["Use 300+ DPI scan", "Try a different OCR engine", "Enter text manually"]
  }
}
```

**Errors:**
| Code | Cause |
|------|-------|
| `MODEL_NOT_FOUND` | Specified model not downloaded |
| `OCR_FAILED` | OCR could not extract text |
| `LLM_FAILED` | LLM inference error |
| `OUT_OF_MEMORY` | System RAM insufficient |
| `CANCELLED` | User cancelled processing |

---

## Command: `get_document`

**Description:** Get document metadata

```
invoke('get_document', { document_id: 'doc-uuid-1234' })
```

**Request:**
```json
{
  "document_id": "doc-uuid-1234",
  "include_full_text": false
}
```

**Response:**
```json
{
  "document_id": "doc-uuid-1234",
  "title": "Quantum Mechanics",
  "file_type": "pdf",
  "file_size_bytes": 24500000,
  "page_count": 240,
  "status": "processed",
  "collections": ["physics", "quantum"],
  "tags": ["quantum-mechanics", "wave-function"],
  "created_at": "2026-07-03T10:30:00Z",
  "processed_at": "2026-07-03T10:31:22Z",
  "stats": {
    "notes_count": 145,
    "flashcards_count": 22,
    "quiz_count": 10,
    "diagrams_count": 3
  },
  "processing_duration_seconds": 82
}
```

---

## Command: `list_documents`

**Description:** List all documents with optional filters

```
invoke('list_documents', { filters: {...}, pagination: {...} })
```

**Request:**
```json
{
  "filters": {
    "collection_id": "optional",
    "status": "processed",
    "search": "quantum",
    "sort_by": "created_at",
    "sort_order": "desc"
  },
  "pagination": {
    "offset": 0,
    "limit": 50
  }
}
```

**Response:**
```json
{
  "documents": [
    {
      "document_id": "doc-uuid-1234",
      "title": "Quantum Mechanics",
      "file_type": "pdf",
      "status": "processed",
      "created_at": "2026-07-03T10:30:00Z",
      "stats": {"notes_count": 145, "flashcards_count": 22}
    }
  ],
  "total": 12,
  "offset": 0,
  "limit": 50
}
```

---

## Command: `delete_document`

**Description:** Delete a document and all its generated content

```
invoke('delete_document', { document_id: 'doc-uuid-1234' })
```

**Response:**
```json
{
  "success": true,
  "freed_bytes": 25000000
}
```

---

## Command: `get_notes`

**Description:** Get generated Markdown notes for a document

```
invoke('get_notes', { document_id: 'doc-uuid-1234' })
```

**Response:**
```json
{
  "document_id": "doc-uuid-1234",
  "markdown": "# Quantum Mechanics\n\n## Overview\n...",
  "format": "markdown",
  "generated_at": "2026-07-03T10:31:22Z"
}
```

---

## Command: `update_notes`

**Description:** Update user-edited notes

```
invoke('update_notes', { document_id: 'doc-uuid-1234', markdown: '...' })
```

**Response:**
```json
{
  "success": true,
  "version": 2,
  "updated_at": "2026-07-03T11:00:00Z"
}
```

---

## Command: `get_flashcards`

**Description:** Get flashcards for a document

```
invoke('get_flashcards', { document_id: 'doc-uuid-1234', filters: {...} })
```

**Request:**
```json
{
  "document_id": "doc-uuid-1234",
  "filters": {
    "difficulty": "all",
    "tags": ["quantum"],
    "limit": 50,
    "offset": 0
  }
}
```

**Response:**
```json
{
  "flashcards": [
    {
      "id": "card-uuid-0001",
      "front": "What is the Schrödinger equation?",
      "back": "The fundamental equation...",
      "type": "qa",
      "difficulty": 0.65,
      "tags": ["quantum", "equations"],
      "source_page": 12,
      "created_at": "2026-07-03T10:31:22Z"
    }
  ],
  "total": 22,
  "offset": 0,
  "limit": 50
}
```

---

## Command: `review_flashcard`

**Description:** Submit flashcard review rating

```
invoke('review_flashcard', { card_id: 'card-uuid-0001', rating: 3 })
```

**Request:**
```json
{
  "card_id": "card-uuid-0001",
  "rating": 3,
  "response_time_ms": 4500
}
```

**Rating Scale:**
| Value | Label | Interval |
|-------|-------|----------|
| 0 | Again | 1 minute |
| 1 | Hard | 5 minutes |
| 2 | Good | 1 day |
| 3 | Easy | 3 days |

**Response:**
```json
{
  "success": true,
  "next_review_at": "2026-07-04T11:00:00Z",
  "interval_days": 1,
  "ease_factor": 2.5
}
```

---

## Command: `get_review_queue`

**Description:** Get due flashcards for spaced repetition

```
invoke('get_review_queue', { limit: 20 })
```

**Response:**
```json
{
  "cards": [...],
  "stats": {
    "due_today": 15,
    "studied_today": 25,
    "retention_rate": 0.88,
    "streak_days": 5
  }
}
```

---

## Command: `get_quiz`

**Description:** Get quiz questions for a document

```
invoke('get_quiz', { document_id: 'doc-uuid-1234', difficulty: 'medium', count: 10 })
```

**Response:**
```json
{
  "questions": [
    {
      "id": "quiz-uuid-0001",
      "type": "mcq",
      "question": "Which equation describes the time evolution of a quantum state?",
      "options": [
        {"label": "A", "text": "Newton's Second Law"},
        {"label": "B", "text": "Schrödinger Equation"},
        {"label": "C", "text": "Maxwell's Equations"},
        {"label": "D", "text": "Einstein's Field Equations"}
      ],
      "correct_answer": "B",
      "explanation": "The Schrödinger equation governs how quantum states evolve over time.",
      "source_page": 5,
      "difficulty": "easy",
      "topic": "wave-function"
    }
  ],
  "total": 10,
  "difficulty": "medium"
}
```

---

## Command: `submit_quiz_answer`

**Description:** Submit quiz answer

```
invoke('submit_quiz_answer', { question_id: 'quiz-uuid-0001', answer: 'B', session_id: '...' })
```

**Response:**
```json
{
  "correct": true,
  "correct_answer": "B",
  "explanation": "...",
  "score_so_far": {"correct": 3, "total": 5}
}
```

---

## Command: `get_diagrams`

**Description:** Get generated diagrams for a document

```
invoke('get_diagrams', { document_id: 'doc-uuid-1234' })
```

**Response:**
```json
{
  "diagrams": [
    {
      "id": "diag-uuid-0001",
      "type": "flowchart",
      "title": "Wave-Particle Duality",
      "mermaid_code": "flowchart TD\n  A[Light] --> B{Wave or Particle?}...",
      "svg_data": "<svg>...</svg>",
      "source_section": "Chapter 1"
    }
  ]
}
```

---

## Command: `get_knowledge_graph`

**Description:** Get knowledge graph data for a document or entire library

```
invoke('get_knowledge_graph', { scope: 'document', document_id: 'doc-uuid-1234' })
invoke('get_knowledge_graph', { scope: 'all', filters: { collection_id: '...' } })
```

**Response:**
```json
{
  "nodes": [
    {
      "id": "concept-wave-function",
      "name": "Wave Function",
      "type": "concept",
      "documents": ["doc-uuid-1234"],
      "strength": 0.95,
      "page_refs": [{"doc": "...", "page": 5}]
    }
  ],
  "edges": [
    {
      "source": "concept-wave-function",
      "target": "concept-schrodinger-equation",
      "relationship": "governs",
      "strength": 0.9
    }
  ]
}
```

---

## Command: `chat_ask`

**Description:** Ask AI a question about a document

```
invoke('chat_ask', { document_id: 'doc-uuid-1234', message: 'Explain...', session_id: '...' })
```

**Response (streaming via event):**
```json
{"event": "chat:token", "data": {"token": "The", "session_id": "..."}}
{"event": "chat:token", "data": {"token": " Schrödinger", "session_id": "..."}}
{"event": "chat:token", "data": {"token": " equation", "session_id": "..."}}
...
{"event": "chat:complete", "data": {"session_id": "...", "citations": [{"page": 5, "text": "..."}]}}
```

**Error:**
```json
{"event": "chat:error", "data": {"code": "MODEL_NOT_LOADED", "message": "..."}}
```

---

## Command: `chat_history`

**Description:** Get chat history for a session or document

```
invoke('chat_history', { document_id: 'doc-uuid-1234', limit: 50 })
```

**Response:**
```json
{
  "messages": [
    {"role": "user", "content": "Explain...", "timestamp": "..."},
    {"role": "assistant", "content": "...", "citations": [...], "timestamp": "..."}
  ]
}
```

---

## Command: `search`

**Description:** Semantic search across all documents

```
invoke('search', { query: 'neural networks backpropagation', limit: 20 })
```

**Request:**
```json
{
  "query": "neural networks backpropagation",
  "filters": {
    "document_ids": [],
    "collections": [],
    "date_from": "2026-01-01",
    "date_to": null
  },
  "limit": 20,
  "offset": 0
}
```

**Response:**
```json
{
  "results": [
    {
      "document_id": "doc-uuid-5678",
      "document_title": "Deep Learning",
      "page_number": 42,
      "snippet": "...backpropagation computes the gradient of the loss function with respect to the weights of the **neural network**...",
      "score": 0.95,
      "concept_matches": ["backpropagation", "neural-network", "gradient-descent"]
    }
  ],
  "total": 12,
  "query_time_ms": 35
}
```

---

## Command: `export_document`

**Description:** Export document to specified format

```
invoke('export_document', { document_id: 'doc-uuid-1234', format: 'markdown', options: {...} })
```

**Request:**
```json
{
  "document_id": "doc-uuid-1234",
  "format": "anki",
  "options": {
    "include_flashcards": true,
    "include_quiz": false,
    "include_diagrams": true,
    "output_path": "/home/user/exports/"
  }
}
```

**Response:**
```json
{
  "success": true,
  "output_path": "/home/user/exports/quantum-mechanics.apkg",
  "file_size_bytes": 2400000,
  "format": "anki",
  "items_exported": {"flashcards": 22, "diagrams": 3}
}
```

**Supported Formats:**
| Format | Extension | Description |
|--------|-----------|-------------|
| `markdown` | .md | Complete notes + flashcards + quiz in Markdown |
| `anki` | .apkg | Anki package with flashcards |
| `pdf` | .pdf | Formatted PDF document |
| `latex` | .tex | LaTeX document |
| `json` | .json | Structured data |
| `csv` | .csv | Flashcards as CSV |
| `txt` | .txt | Plain text |

---

## Command: `get_models`

**Description:** List available and installed AI models

```
invoke('get_models', {})
```

**Response:**
```json
{
  "models": [
    {
      "id": "tesseract-v5",
      "type": "ocr",
      "name": "Tesseract v5",
      "size_bytes": 45000000,
      "installed": true,
      "version": "5.3.3",
      "languages": ["en", "hi", "fr", "de", "es", "zh"]
    },
    {
      "id": "llama-3.2-1b",
      "type": "llm",
      "name": "Llama 3.2 1B",
      "size_bytes": 620000000,
      "installed": false,
      "download_url": "https://huggingface.co/...",
      "ram_required_mb": 1024,
      "quantization": "Q4_K_M",
      "format": "gguf"
    }
  ],
  "storage_used_bytes": 1200000000,
  "storage_total_bytes": 10000000000
}
```

---

## Command: `download_model`

**Description:** Download an AI model

```
invoke('download_model', { model_id: 'llama-3.2-1b' })
```

**Progress Events:**
```json
{"event": "download:progress", "data": {"model_id": "...", "downloaded_bytes": 310000000, "total_bytes": 620000000, "speed_mbps": 45}}
```

---

## Command: `collections_list`

**Description:** List all collections

```
invoke('collections_list', {})
```

---

## Command: `collection_create`

**Description:** Create a new collection

```
invoke('collection_create', { name: 'Physics', description: '...', color: '#6366F1' })
```

---

## Command: `collection_add_document`

**Description:** Add document to collection

```
invoke('collection_add_document', { collection_id: '...', document_id: 'doc-uuid-1234' })
```

---

## Command: `get_settings`

**Description:** Get all user settings

```
invoke('get_settings', {})
```

---

## Command: `update_settings`

**Description:** Update user settings

```
invoke('update_settings', { theme: 'dark', font_size: 'lg', ... })
```

---

## Command: `get_memory`

**Description:** Get AI memory data

```
invoke('get_memory', { type: 'all' })
invoke('get_memory', { type: 'progress' })
invoke('get_memory', { type: 'corrections' })
```

---

## Command: `clear_memory`

**Description:** Clear AI memory

```
invoke('clear_memory', { types: ['corrections', 'interactions'] })
```

---

## Command: `get_stats`

**Description:** Get usage statistics

```
invoke('get_stats', {})
```

**Response:**
```json
{
  "total_documents": 15,
  "total_flashcards": 320,
  "cards_reviewed_today": 25,
  "quiz_taken": 12,
  "average_quiz_score": 0.78,
  "retention_rate": 0.85,
  "streak_days": 7,
  "storage_used_bytes": 2400000000,
  "active_time_minutes": 1240
}
```
