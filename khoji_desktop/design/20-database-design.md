# Database Design

Khoji uses **SQLite** for all structured data and **sqlite-vec** for vector embeddings (loaded as a SQLite extension). All data is stored locally in `~/.khoji/db/`.

---

## Database: `khoji.db` (Main Database)

### Table: `documents`

```sql
CREATE TABLE documents (
    id              TEXT PRIMARY KEY,           -- UUID
    title           TEXT NOT NULL,              -- Extracted or original filename
    file_type       TEXT NOT NULL,              -- 'pdf', 'png', 'jpg', 'ppt', 'pptx', 'doc', 'docx', 'epub'
    file_path       TEXT NOT NULL UNIQUE,       -- Absolute path to original file
    file_size_bytes INTEGER NOT NULL,
    page_count      INTEGER,
    status          TEXT NOT NULL DEFAULT 'uploaded',  -- 'uploaded', 'processing', 'processed', 'failed'
    error_message   TEXT,
    processing_duration_seconds REAL,
    metadata_json   TEXT,                       -- JSON: author, title, subject from PDF metadata
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    processed_at    TEXT,
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_created ON documents(created_at);
CREATE INDEX idx_documents_title ON documents(title);
```

### Table: `document_chunks`

```sql
CREATE TABLE document_chunks (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index     INTEGER NOT NULL,
    content         TEXT NOT NULL,
    token_count     INTEGER NOT NULL,
    page_start      INTEGER,
    page_end        INTEGER,
    section         TEXT,                       -- 'title', 'abstract', 'body', 'figure', 'table', 'formula'
    embedding_id    TEXT,                       -- Reference to vectors table
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_chunks_document ON document_chunks(document_id);
CREATE INDEX idx_chunks_section ON document_chunks(section);
```

### Table: `notes`

```sql
CREATE TABLE notes (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    markdown        TEXT NOT NULL,              -- Full Markdown notes
    version         INTEGER NOT NULL DEFAULT 1,
    is_user_edited  INTEGER NOT NULL DEFAULT 0,
    generated_at    TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_notes_document ON notes(document_id);
```

### Table: `flashcards`

```sql
CREATE TABLE flashcards (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    front           TEXT NOT NULL,
    back            TEXT NOT NULL,
    card_type       TEXT NOT NULL,              -- 'qa', 'cloze', 'image_occlusion'
    difficulty      REAL NOT NULL DEFAULT 0.5, -- 0.0 (easy) to 1.0 (hard)
    tags            TEXT,                       -- JSON array: ["quantum", "equations"]
    source_page     INTEGER,
    source_chunk_id TEXT REFERENCES document_chunks(id),
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_flashcards_document ON flashcards(document_id);
CREATE INDEX idx_flashcards_tags ON flashcards(tags);
CREATE INDEX idx_flashcards_difficulty ON flashcards(difficulty);
```

### Table: `flashcard_reviews`

```sql
CREATE TABLE flashcard_reviews (
    id              TEXT PRIMARY KEY,
    card_id         TEXT NOT NULL REFERENCES flashcards(id) ON DELETE CASCADE,
    rating          INTEGER NOT NULL CHECK(rating >= 0 AND rating <= 3), -- 0=again, 1=hard, 2=good, 3=easy
    response_time_ms INTEGER,
    reviewed_at     TEXT NOT NULL DEFAULT (datetime('now')),
    
    -- SM-2/FSRS state
    ease_factor     REAL NOT NULL DEFAULT 2.5,
    interval_days   REAL NOT NULL DEFAULT 0,
    repetitions     INTEGER NOT NULL DEFAULT 0,
    next_review_at  TEXT NOT NULL,
    
    session_id      TEXT                     -- groups reviews into sessions
);

CREATE INDEX idx_reviews_card ON flashcard_reviews(card_id);
CREATE INDEX idx_reviews_next ON flashcard_reviews(next_review_at);
CREATE INDEX idx_reviews_session ON flashcard_reviews(session_id);
```

### Table: `quiz_questions`

```sql
CREATE TABLE quiz_questions (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    question_type   TEXT NOT NULL,              -- 'mcq', 'true_false', 'fill_blank', 'matching', 'ordering'
    question_text   TEXT NOT NULL,
    options         TEXT,                       -- JSON array for MCQ options
    correct_answer  TEXT NOT NULL,
    explanation     TEXT,
    difficulty      TEXT NOT NULL DEFAULT 'medium', -- 'easy', 'medium', 'hard'
    topic           TEXT,
    source_page     INTEGER,
    source_chunk_id TEXT REFERENCES document_chunks(id),
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_quiz_document ON quiz_questions(document_id);
CREATE INDEX idx_quiz_difficulty ON quiz_questions(difficulty);
CREATE INDEX idx_quiz_topic ON quiz_questions(topic);
```

### Table: `quiz_sessions`

```sql
CREATE TABLE quiz_sessions (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    difficulty      TEXT NOT NULL DEFAULT 'medium',
    question_count  INTEGER NOT NULL,
    correct_count   INTEGER DEFAULT 0,
    score_pct       REAL,
    started_at      TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at    TEXT,
    duration_seconds REAL
);
```

### Table: `quiz_answers`

```sql
CREATE TABLE quiz_answers (
    id              TEXT PRIMARY KEY,
    session_id      TEXT NOT NULL REFERENCES quiz_sessions(id) ON DELETE CASCADE,
    question_id     TEXT NOT NULL REFERENCES quiz_questions(id),
    user_answer     TEXT NOT NULL,
    is_correct      INTEGER NOT NULL,
    response_time_ms INTEGER
);

CREATE INDEX idx_quiz_answers_session ON quiz_answers(session_id);
```

### Table: `diagrams`

```sql
CREATE TABLE diagrams (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    diagram_type    TEXT NOT NULL,              -- 'flowchart', 'mindmap', 'timeline', 'er', 'sequence', 'class', 'graph'
    title           TEXT NOT NULL,
    mermaid_code    TEXT NOT NULL,
    svg_data        TEXT,                       -- Cached SVG for fast rendering
    source_section  TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_diagrams_document ON diagrams(document_id);
CREATE INDEX idx_diagrams_type ON diagrams(diagram_type);
```

### Table: `collections`

```sql
CREATE TABLE collections (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    description     TEXT,
    color           TEXT DEFAULT '#6366F1',
    icon            TEXT DEFAULT 'folder',
    parent_id       TEXT REFERENCES collections(id) ON DELETE SET NULL,
    is_smart        INTEGER NOT NULL DEFAULT 0,    -- Auto-collection based on rules
    smart_rules     TEXT,                           -- JSON: conditions for smart collection
    sort_order      INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_collections_parent ON collections(parent_id);
```

### Table: `collection_documents`

```sql
CREATE TABLE collection_documents (
    collection_id   TEXT NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    added_at        TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (collection_id, document_id)
);

CREATE INDEX idx_coll_doc_document ON collection_documents(document_id);
```

### Table: `concepts` (Knowledge Graph)

```sql
CREATE TABLE concepts (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    concept_type    TEXT NOT NULL,              -- 'principle', 'formula', 'algorithm', 'definition', 'person', 'date', 'dataset', 'tool', 'code', 'question'
    description     TEXT,
    tags            TEXT,                       -- JSON array
    confidence      REAL NOT NULL DEFAULT 1.0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_concepts_type ON concepts(concept_type);
CREATE INDEX idx_concepts_name ON concepts(name);
```

### Table: `concept_documents`

```sql
CREATE TABLE concept_documents (
    concept_id      TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_refs       TEXT,                       -- JSON array of page numbers
    strength        REAL NOT NULL DEFAULT 1.0,
    PRIMARY KEY (concept_id, document_id)
);
```

### Table: `concept_relationships`

```sql
CREATE TABLE concept_relationships (
    id              TEXT PRIMARY KEY,
    source_id       TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    target_id       TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    relationship    TEXT NOT NULL,              -- 'uses', 'requires', 'causes', 'is_a', 'has', 'contradicts', 'related_to'
    strength        REAL NOT NULL DEFAULT 1.0,
    discovered_in   TEXT REFERENCES documents(id),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(source_id, target_id, relationship)
);

CREATE INDEX idx_relationships_source ON concept_relationships(source_id);
CREATE INDEX idx_relationships_target ON concept_relationships(target_id);
```

### Table: `chat_sessions`

```sql
CREATE TABLE chat_sessions (
    id              TEXT PRIMARY KEY,
    document_id     TEXT REFERENCES documents(id) ON DELETE CASCADE,
    title           TEXT,
    message_count   INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_chat_document ON chat_sessions(document_id);
```

### Table: `chat_messages`

```sql
CREATE TABLE chat_messages (
    id              TEXT PRIMARY KEY,
    session_id      TEXT NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role            TEXT NOT NULL,              -- 'user', 'assistant', 'system'
    content         TEXT NOT NULL,
    citations       TEXT,                       -- JSON array of {page, text, document_id}
    tokens_used     INTEGER,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_messages_session ON chat_messages(session_id);
```

### Table: `ai_memory` (General Memory KV Store)

```sql
CREATE TABLE ai_memory (
    key             TEXT PRIMARY KEY,           -- 'preference:style', 'progress:quantum-mechanics', etc.
    value           TEXT NOT NULL,              -- JSON value
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### Table: `ai_corrections`

```sql
CREATE TABLE ai_corrections (
    id              TEXT PRIMARY KEY,
    original_output TEXT NOT NULL,
    user_correction TEXT NOT NULL,
    context         TEXT,                       -- JSON: document_id, concept_id, etc.
    applied_count   INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### Table: `user_settings`

```sql
CREATE TABLE user_settings (
    key             TEXT PRIMARY KEY,
    value           TEXT NOT NULL               -- JSON value
);

-- Default settings inserted on first run
INSERT INTO user_settings VALUES ('theme', '"dark"');
INSERT INTO user_settings VALUES ('font_size', '"md"');
INSERT INTO user_settings VALUES ('reading_mode', '"sans"');
INSERT INTO user_settings VALUES ('language', '"en"');
INSERT INTO user_settings VALUES ('show_sidebar', 'true');
INSERT INTO user_settings VALUES ('default_export_format', '"markdown"');
INSERT INTO user_settings VALUES ('model_ocr', '"tesseract-v5"');
INSERT INTO user_settings VALUES ('model_embedding', '"all-minilm-l6-v2"');
INSERT INTO user_settings VALUES ('model_llm', '"llama-3.2-1b"');
```

### Table: `processing_jobs`

```sql
CREATE TABLE processing_jobs (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    status          TEXT NOT NULL DEFAULT 'queued', -- 'queued', 'running', 'completed', 'failed', 'cancelled'
    current_stage   TEXT,
    stage_index     INTEGER DEFAULT 0,
    total_stages    INTEGER NOT NULL,
    progress_pct    REAL DEFAULT 0.0,
    error_message   TEXT,
    started_at      TEXT,
    completed_at    TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_jobs_status ON processing_jobs(status);
```

---

## Database: `vectors.db` (Vector Embeddings)

Loaded as a SQLite extension via `sqlite-vec`.

```sql
-- The sqlite-vec extension provides virtual tables for vector storage
-- Schema is defined here for reference

-- Each document chunk gets an embedding vector
CREATE VIRTUAL TABLE chunk_embeddings USING vec0(
    chunk_id TEXT PRIMARY KEY,
    embedding FLOAT[384] distance_metric=cosine
);

-- Knowledge graph concepts also get embeddings
CREATE VIRTUAL TABLE concept_embeddings USING vec0(
    concept_id TEXT PRIMARY KEY,
    embedding FLOAT[384] distance_metric=cosine
);

-- Chat queries can be cached for fast repeated search
CREATE VIRTUAL TABLE query_embeddings USING vec0(
    query_hash TEXT PRIMARY KEY,
    embedding FLOAT[384] distance_metric=cosine
);
```

---

## Entity Relationship Diagram (Simplified)

```
documents ──1:N── document_chunks ──1:1── chunk_embeddings
    │
    ├──1:1── notes
    ├──1:N── flashcards ──1:N── flashcard_reviews
    ├──1:N── quiz_questions
    ├──1:N── diagrams
    ├──1:N── chat_sessions ──1:N── chat_messages
    └──1:N── concept_documents ──N:1── concepts ──1:N── concept_relationships
                                        │
                                        └──1:1── concept_embeddings

collections ──N:M── documents (via collection_documents)

ai_memory        (key-value store)
ai_corrections   (correction log)
user_settings    (key-value store)
processing_jobs  (job queue)
```

---

## Indexes Summary

| Table | Indexes | Purpose |
|-------|---------|---------|
| documents | status, created_at, title | Listing, filtering, sorting |
| document_chunks | document_id, section | Chunk retrieval by doc |
| notes | document_id | Fast note lookup |
| flashcards | document_id, tags, difficulty | Card listing & filtering |
| flashcard_reviews | card_id, next_review_at, session_id | Review queue |
| quiz_questions | document_id, difficulty, topic | Quiz generation |
| quiz_answers | session_id | Session scoring |
| diagrams | document_id, type | Diagram listing |
| collections | parent_id | Hierarchy |
| concepts | type, name | Graph lookup |
| concept_relationships | source_id, target_id | Graph traversal |
| chat_sessions | document_id | Session management |
| chat_messages | session_id | Message history |
| processing_jobs | status | Job queue |
| chunk_embeddings | (vector index) | Similarity search |
| concept_embeddings | (vector index) | Concept similarity |
