/* ==========================================================================
   KHOJI PORTAL INTERACTION LOGIC (docs/script.js)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // ── Theme System ────────────────────────────────────────────────────────
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  
  function getPreferredTheme() {
    const savedTheme = localStorage.getItem('color-scheme');
    if (savedTheme) return savedTheme;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('color-scheme', theme);
    const metaTheme = document.querySelector('meta[name="color-scheme"]');
    if (metaTheme) {
      metaTheme.content = theme === 'dark' ? 'dark' : 'light';
    }
  }

  // Initialize theme
  const initialTheme = getPreferredTheme();
  setTheme(initialTheme);

  // Toggle theme button listener
  themeToggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  });

  // Watch system preferences for theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('color-scheme')) {
      setTheme(e.matches ? 'dark' : 'light');
    }
  });

  // ── Navigation & Sidebar ────────────────────────────────────────────────
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('.doc-section');
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const sidebar = document.querySelector('.sidebar');

  function switchSection(targetId) {
    sections.forEach(sec => {
      sec.classList.remove('active');
      if (sec.id === targetId) sec.classList.add('active');
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('data-section') === targetId) {
        link.classList.add('active');
      }
    });

    // Scroll to top of content
    window.scrollTo({ top: 0, behavior: 'instant' });
    
    // Close sidebar on mobile
    sidebar.classList.remove('mobile-open');
  }

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetSection = link.getAttribute('data-section');
      switchSection(targetSection);
      window.location.hash = targetSection;
    });
  });

  // Handle URL hashes on load
  if (window.location.hash) {
    const hash = window.location.hash.substring(1);
    const targetSection = document.getElementById(hash);
    if (targetSection && targetSection.classList.contains('doc-section')) {
      switchSection(hash);
    }
  }

  // Mobile menu button
  mobileMenuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('mobile-open');
  });

  // Close sidebar on outer click on mobile
  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768) {
      if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target) && sidebar.classList.contains('mobile-open')) {
        sidebar.classList.remove('mobile-open');
      }
    }
  });

  // ── Clipboard Copy (Terminal Code Block) ─────────────────────────────────
  const copyBtn = document.getElementById('copyBtn');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const codeElement = copyBtn.closest('.terminal-block').querySelector('.terminal-code');
      const textToCopy = codeElement.textContent.trim();
      
      navigator.clipboard.writeText(textToCopy).then(() => {
        const originalHTML = copyBtn.innerHTML;
        copyBtn.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check"><path d="M20 6 9 17l-5-5"/></svg>
          Copied!
        `;
        copyBtn.style.borderColor = 'var(--color-success-500)';
        copyBtn.style.color = 'var(--color-success-500)';
        
        setTimeout(() => {
          copyBtn.innerHTML = originalHTML;
          copyBtn.style.borderColor = '';
          copyBtn.style.color = '';
        }, 2000);
      });
    });
  }

  // ── Interactive Multi-Agent Pipeline Data & Logic ───────────────────────
  const pipelineSteps = document.querySelectorAll('.pipeline-step');
  const activeAgentTitle = document.getElementById('activeAgentTitle');
  const agentDetailsBody = document.getElementById('agentDetailsBody');

  const pipelineData = {
    'input': {
      title: 'Phase 1: Input & Ingestion',
      desc: 'Supports multi-format uploads (PDF, images, EPUB, docx) and triggers the processing job queue.',
      agents: ['ocr', 'layout', 'vision']
    },
    'extraction': {
      title: 'Phase 2: Structured Parsing & OCR',
      desc: 'Converts raw bytes and scanned pages into structural text chunks using OCR fallbacks and visual modeling.',
      agents: ['ocr', 'layout', 'vision', 'extraction']
    },
    'indexing': {
      title: 'Phase 3: Semantic Indexing & Vector Search',
      desc: 'Embeds text chunks into 384-dimensional vector spaces and populates SQLite vector extensions.',
      agents: ['extraction', 'graph', 'review']
    },
    'synthesis': {
      title: 'Phase 4: Synthesis & Learning Generation',
      desc: 'Invokes localized reasoning models to compile summaries, flashcards, MCQs, and Mermaid diagrams.',
      agents: ['reasoning', 'flashcard', 'quiz', 'diagram', 'markdown']
    },
    'export': {
      title: 'Phase 5: Output & Sync',
      desc: 'Packages generated structured markdown, Anki decks, and CSV quiz databases for user download.',
      agents: ['markdown', 'review', 'export']
    }
  };

  const agentSpecifications = {
    'ocr': {
      name: 'OCR Agent (Agent 1)',
      desc: 'Responsible for text region detection and character recognition in scanned documents or image inputs.',
      models: 'Tesseract v5, Surya OCR, EasyOCR, PaddleOCR fallback',
      input: 'Document pages or image files (PNG, JPG, PDF pages)',
      output: 'Raw extracted text strings mapped with bounding boxes and confidence metrics.',
      lowMemory: 'Tesseract v5 (CPU native)',
      highMemory: 'Surya OCR (GPU accelerated)'
    },
    'layout': {
      name: 'Layout Analysis Agent (Agent 2)',
      desc: 'Analyzes document reading order and segments the text into functional blocks like headings, tables, formulas, footers.',
      models: 'LayoutLMv3, Detectron2, Heuristic rules fallback',
      input: 'PDF layout coordinates + page render raster images',
      output: 'Hierarchical structural coordinate boxes classified by content type (e.g. title, figure, table).',
      lowMemory: 'Rule-based coordinate geometry heuristic',
      highMemory: 'LayoutLMv3 deep semantic layout model'
    },
    'vision': {
      name: 'Vision Agent (Agent 3)',
      desc: 'Extracts data tables, describes figures, and transcribes visual charts into structured textual captions.',
      models: 'Florence-2, Qwen2-VL, None fallback (skips if < 8GB RAM)',
      input: 'Cropped layout elements containing charts, drawings, or diagrams',
      output: 'Textual data tables, schematic descriptions, or anatomical legends.',
      lowMemory: 'Skip execution (graceful degradation)',
      highMemory: 'Florence-2 (base/large)'
    },
    'extraction': {
      name: 'Knowledge Extraction Agent (Agent 4)',
      desc: 'Analyzes structured text block chunks and extracts key terminology definitions and logical relationships.',
      models: 'Llama-3.2-1B, Phi-3 Mini 3.8B, Mistral 7B',
      input: 'Structured text segments + layout classification JSON',
      output: 'Knowledge graph node objects (concepts, formulas, people) and edges (dependencies, causes).',
      lowMemory: 'Llama-3.2-1B (Q4_K_M)',
      highMemory: 'Mistral-7B-Instruct (Q8_0)'
    },
    'reasoning': {
      name: 'Reasoning Agent (Agent 5)',
      desc: 'Generates multi-level textual explanations, real-world analogies, and reading comprehension questions.',
      models: 'Llama-3.2-1B, Phi-3 Mini 3.8B, Mistral 7B',
      input: 'Raw text chunks + concept metadata',
      output: 'Markdown summaries (TL;DR, Beginner, Expert levels), logical cause-effect descriptions.',
      lowMemory: 'Llama-3.2-1B (auto-routed)',
      highMemory: 'Phi-3-Mini (3.8B)'
    },
    'graph': {
      name: 'Knowledge Graph Agent (Agent 6)',
      desc: 'Algorithmic agent that merges extracted local concepts into a global multi-document SQLite database. Computes node centrality.',
      models: 'Network centrality algorithms, SQL graph traversals',
      input: 'Extracted concept lists and relationship pairs',
      output: 'Updated global SQLite knowledge graph structures, community clusters, and suggested learning paths.',
      lowMemory: 'In-memory list traversal',
      highMemory: 'SQLite-vec semantic concept merging'
    },
    'flashcard': {
      name: 'Flashcard Agent (Agent 7)',
      desc: 'Formulates flashcards (cloze-deletions and question-answer pairs) calibrated for spaced repetition.',
      models: 'Llama-3.2-1B fine-tuned, Rule-based extractor fallback',
      input: 'Concept definitions, formulas, and highlighted facts',
      output: 'Array of flashcard records complete with front/back copy, types, and source context.',
      lowMemory: 'Rule-based sentence extraction templates',
      highMemory: 'Llama-3.2-1B card generator prompt'
    },
    'quiz': {
      name: 'Quiz Agent (Agent 8)',
      desc: 'Creates multiple-choice, true/false, and match-up quizzes, ensuring distractors are semantically plausible.',
      models: 'Llama-3.2-1B, Phi-3 Mini',
      input: 'Document sections, extracted key concept schemas',
      output: 'Array of quiz questions complete with MCQ options, correct answer indexes, and logic explanations.',
      lowMemory: 'Llama-3.2-1B template prompt',
      highMemory: 'Phi-3-Mini structured JSON generator'
    },
    'diagram': {
      name: 'Diagram Agent (Agent 9)',
      desc: 'Compiles processes, timelines, or structural classifications into rendering-compliant Mermaid syntax.',
      models: 'Llama-3.2-1B, PlantUML / Mermaid template renderer',
      input: 'Logical event sequences or hierarchical concept links',
      output: 'Mermaid.js text syntax representing flowcharts, mindmaps, or timeline tracks.',
      lowMemory: 'Pre-defined structural templates',
      highMemory: 'LLM fine-tuned for code generation'
    },
    'markdown': {
      name: 'Markdown Formatting Agent (Agent 10)',
      desc: 'Assembles note summaries, diagrams, and metadata into a comprehensive, styled Markdown workspace document.',
      models: 'Llama-3.2-1B, templated markdown builders',
      input: 'All outputs generated by parsing, reasoning, and diagram agents',
      output: 'Structured Markdown file (.md) complete with metadata frontmatter and asset references.',
      lowMemory: 'Template compiler',
      highMemory: 'Llama-3.2-1B layout compiler'
    },
    'review': {
      name: 'Review & Spaced Repetition Agent (Agent 11)',
      desc: 'Calculates intervals and reviews using the FSRS or SM-2 algorithms based on historical ratings.',
      models: 'SM-2 / FSRS scheduling formulas',
      input: 'User review ratings (Again, Hard, Good, Easy) + repetition records',
      output: 'Updated intervals, ease factors, and card review schedules for the SQLite database.',
      lowMemory: 'Native Python math implementation',
      highMemory: 'FSRS optimization algorithms'
    },
    'export': {
      name: 'Export Agent (Agent 12)',
      desc: 'Translates workspace knowledge assets into external formats such as Anki APKG decks, PDF layouts, or structured CSVs.',
      models: 'Anki deck compilers, LaTeX compilers, CSV exporters',
      input: 'Compiled SQLite records, Markdown documents, and settings',
      output: 'Export files (.apkg, .pdf, .json, .csv) saved directly to the user\'s local disk.',
      lowMemory: 'Python standard library exporters',
      highMemory: 'LaTeX engine PDF compilers'
    }
  };

  function selectPipelinePhase(phaseKey) {
    const data = pipelineData[phaseKey];
    if (!data) return;

    // Highlight active phase button
    pipelineSteps.forEach(step => {
      step.classList.remove('active');
      if (step.getAttribute('data-phase') === phaseKey) {
        step.classList.add('active');
      }
    });

    // Populate phase title & description
    activeAgentTitle.innerHTML = `
      <h3>${data.title}</h3>
      <p style="margin-top: 4px; font-weight: 500; color: var(--text-secondary);">${data.desc}</p>
    `;

    // Render agents linked with this phase
    let cardsHtml = '<div class="agent-card-grid">';
    data.agents.forEach(agentKey => {
      const agent = agentSpecifications[agentKey];
      cardsHtml += `
        <div class="agent-grid-item" data-agent="${agentKey}">
          <div>
            <h4>${agent.name}</h4>
            <p style="font-size: 0.8rem; line-height: 1.4; color: var(--text-secondary); margin-top: 4px;">
              ${agent.desc.substring(0, 75)}...
            </p>
          </div>
          <span class="badge badge-primary" style="margin-top: 8px; width: fit-content;">View Specs</span>
        </div>
      `;
    });
    cardsHtml += '</div>';

    // Container for agent details
    cardsHtml += '<div id="agentDetailViewer" style="margin-top: 24px;"></div>';
    agentDetailsBody.innerHTML = cardsHtml;

    // Connect agent item click listeners
    const agentGridItems = agentDetailsBody.querySelectorAll('.agent-grid-item');
    agentGridItems.forEach(item => {
      item.addEventListener('click', () => {
        const agentKey = item.getAttribute('data-agent');
        showAgentDetails(agentKey);
        
        agentGridItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');
      });
    });

    // Show first agent details by default
    if (data.agents.length > 0) {
      showAgentDetails(data.agents[0]);
      agentGridItems[0].classList.add('active');
    }
  }

  function showAgentDetails(agentKey) {
    const spec = agentSpecifications[agentKey];
    const viewer = document.getElementById('agentDetailViewer');
    if (!spec || !viewer) return;

    viewer.innerHTML = `
      <div class="agent-details-box">
        <div class="agent-details-header">
          <h3>${spec.name}</h3>
          <span class="badge badge-success">${spec.models.split(',')[0]}</span>
        </div>
        <p style="margin-bottom: var(--space-4); line-height: 1.6;">${spec.desc}</p>
        <div class="agent-meta-specs">
          <div class="meta-spec-item">
            <div class="meta-spec-label">Input Format</div>
            <div class="meta-spec-value">${spec.input}</div>
          </div>
          <div class="meta-spec-item">
            <div class="meta-spec-label">Output Data</div>
            <div class="meta-spec-value">${spec.output}</div>
          </div>
          <div class="meta-spec-item">
            <div class="meta-spec-label">RAM Setup (Low)</div>
            <div class="meta-spec-value" style="color: var(--color-warning-600);">${spec.lowMemory}</div>
          </div>
          <div class="meta-spec-item">
            <div class="meta-spec-label">RAM Setup (High)</div>
            <div class="meta-spec-value" style="color: var(--color-primary-600);">${spec.highMemory}</div>
          </div>
        </div>
      </div>
    `;
  }

  pipelineSteps.forEach(step => {
    step.addEventListener('click', () => {
      selectPipelinePhase(step.getAttribute('data-phase'));
    });
  });

  // Initial load default phase selection
  selectPipelinePhase('input');

  // ── SQLite Database Schema Explorer ────────────────────────────────────
  const dbTableButtons = document.querySelectorAll('.db-table-btn');
  const dbSchemaTitle = document.getElementById('dbSchemaTitle');
  const dbSchemaDescription = document.getElementById('dbSchemaDescription');
  const dbSchemaSql = document.getElementById('dbSchemaSql');
  const dbIndexesList = document.getElementById('dbIndexesList');

  const schemasData = {
    'documents': {
      title: 'documents',
      desc: 'Stores global document metadata, file paths, page totals, processing states, and errors.',
      sql: `CREATE TABLE documents (
    id              TEXT PRIMARY KEY,           -- UUID
    title           TEXT NOT NULL,              -- Extracted or original filename
    file_type       TEXT NOT NULL,              -- 'pdf', 'png', 'jpg', 'ppt', 'pptx', etc.
    file_path       TEXT NOT NULL UNIQUE,       -- Absolute path to original file
    file_size_bytes INTEGER NOT NULL,
    page_count      INTEGER,
    status          TEXT NOT NULL DEFAULT 'uploaded',  -- 'uploaded', 'processing', 'processed', 'failed'
    error_message   TEXT,
    processing_duration_seconds REAL,
    metadata_json   TEXT,                       -- JSON: author, title, subject
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    processed_at    TEXT,
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);`,
      indexes: [
        'CREATE INDEX idx_documents_status ON documents(status);',
        'CREATE INDEX idx_documents_created ON documents(created_at);',
        'CREATE INDEX idx_documents_title ON documents(title);'
      ]
    },
    'document_chunks': {
      title: 'document_chunks',
      desc: 'Holds parsed text block divisions mapped to pages, token counts, and embedding references.',
      sql: `CREATE TABLE document_chunks (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index     INTEGER NOT NULL,
    content         TEXT NOT NULL,
    token_count     INTEGER NOT NULL,
    page_start      INTEGER,
    page_end        INTEGER,
    section         TEXT,                       -- 'title', 'abstract', 'body', 'figure', 'table'
    embedding_id    TEXT,                       -- Reference to vectors table
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);`,
      indexes: [
        'CREATE INDEX idx_chunks_document ON document_chunks(document_id);',
        'CREATE INDEX idx_chunks_section ON document_chunks(section);'
      ]
    },
    'notes': {
      title: 'notes',
      desc: 'Stores the unified structured Markdown summary notes generated or edited for the active file.',
      sql: `CREATE TABLE notes (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    markdown        TEXT NOT NULL,              -- Full Markdown notes
    version         INTEGER NOT NULL DEFAULT 1,
    is_user_edited  INTEGER NOT NULL DEFAULT 0,
    generated_at    TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);`,
      indexes: [
        'CREATE INDEX idx_notes_document ON notes(document_id);'
      ]
    },
    'flashcards': {
      title: 'flashcards',
      desc: 'Contains auto-generated flashcards (Q&A or Cloze tests) associated with source file chunks.',
      sql: `CREATE TABLE flashcards (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    front           TEXT NOT NULL,
    back            TEXT NOT NULL,
    card_type       TEXT NOT NULL,              -- 'qa', 'cloze', 'image_occlusion'
    difficulty      REAL NOT NULL DEFAULT 0.5,  -- 0.0 (easy) to 1.0 (hard)
    tags            TEXT,                       -- JSON array: ["quantum", "equations"]
    source_page     INTEGER,
    source_chunk_id TEXT REFERENCES document_chunks(id),
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);`,
      indexes: [
        'CREATE INDEX idx_flashcards_document ON flashcards(document_id);',
        'CREATE INDEX idx_flashcards_tags ON flashcards(tags);',
        'CREATE INDEX idx_flashcards_difficulty ON flashcards(difficulty);'
      ]
    },
    'flashcard_reviews': {
      title: 'flashcard_reviews',
      desc: 'Logs spaced repetition study events and records interval factors computed by FSRS/SM-2.',
      sql: `CREATE TABLE flashcard_reviews (
    id              TEXT PRIMARY KEY,
    card_id         TEXT NOT NULL REFERENCES flashcards(id) ON DELETE CASCADE,
    rating          INTEGER NOT NULL CHECK(rating >= 0 AND rating <= 3), -- 0=again, 1=hard, 2=good, 3=easy
    response_time_ms INTEGER,
    reviewed_at     TEXT NOT NULL DEFAULT (datetime('now')),
    ease_factor     REAL NOT NULL DEFAULT 2.5,
    interval_days   REAL NOT NULL DEFAULT 0,
    repetitions     INTEGER NOT NULL DEFAULT 0,
    next_review_at  TEXT NOT NULL,
    session_id      TEXT                     -- groups reviews into sessions
);`,
      indexes: [
        'CREATE INDEX idx_reviews_card ON flashcard_reviews(card_id);',
        'CREATE INDEX idx_reviews_next ON flashcard_reviews(next_review_at);'
      ]
    },
    'quiz_questions': {
      title: 'quiz_questions',
      desc: 'Maintains MCQ and true/false exam items generated for specific document contexts.',
      sql: `CREATE TABLE quiz_questions (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    question_type   TEXT NOT NULL,              -- 'mcq', 'true_false', 'fill_blank'
    question_text   TEXT NOT NULL,
    options         TEXT,                       -- JSON array for MCQ options
    correct_answer  TEXT NOT NULL,
    explanation     TEXT,
    difficulty      TEXT NOT NULL DEFAULT 'medium', -- 'easy', 'medium', 'hard'
    topic           TEXT,
    source_page     INTEGER,
    source_chunk_id TEXT REFERENCES document_chunks(id),
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);`,
      indexes: [
        'CREATE INDEX idx_quiz_document ON quiz_questions(document_id);',
        'CREATE INDEX idx_quiz_difficulty ON quiz_questions(difficulty);'
      ]
    },
    'concepts': {
      title: 'concepts',
      desc: 'Represents entities and terms extracted to build the global cross-document Knowledge Graph.',
      sql: `CREATE TABLE concepts (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    concept_type    TEXT NOT NULL,              -- \'principle\', \'formula\', \'definition\'
    description     TEXT,
    tags            TEXT,                       -- JSON array
    confidence      REAL NOT NULL DEFAULT 1.0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);`,
      indexes: [
        'CREATE INDEX idx_concepts_type ON concepts(concept_type);',
        'CREATE INDEX idx_concepts_name ON concepts(name);'
      ]
    },
    'concept_relationships': {
      title: 'concept_relationships',
      desc: 'Tracks directional relational lines between concepts (e.g. wave functions govern probability densities).',
      sql: `CREATE TABLE concept_relationships (
    id              TEXT PRIMARY KEY,
    source_id       TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    target_id       TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    relationship    TEXT NOT NULL,              -- \'uses\', \'requires\', \'causes\'
    strength        REAL NOT NULL DEFAULT 1.0,
    discovered_in   TEXT REFERENCES documents(id),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(source_id, target_id, relationship)
);`,
      indexes: [
        'CREATE INDEX idx_relationships_source ON concept_relationships(source_id);',
        'CREATE INDEX idx_relationships_target ON concept_relationships(target_id);'
      ]
    },
    'ai_memory': {
      title: 'ai_memory',
      desc: 'General persistent Key-Value storage tracking topic mastery parameters and personalization states.',
      sql: `CREATE TABLE ai_memory (
    key             TEXT PRIMARY KEY,           -- \'preference:style\', \'progress:quantum-mechanics\', etc.
    value           TEXT NOT NULL,              -- JSON value
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);`,
      indexes: [
        '-- None: Primary key hash access matches Key-Value lookups.'
      ]
    },
    'ai_corrections': {
      title: 'ai_corrections',
      desc: 'Logs corrections inputted by the user to overwrite and override future LLM interpretations.',
      sql: `CREATE TABLE ai_corrections (
    id              TEXT PRIMARY KEY,
    original_output TEXT NOT NULL,
    user_correction TEXT NOT NULL,
    context         TEXT,                       -- JSON: document_id, concept_id
    applied_count   INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);`,
      indexes: [
        '-- None: Accessed sequentially by orchestrators for pattern matches.'
      ]
    },
    'chunk_embeddings': {
      title: 'chunk_embeddings (vectors.db)',
      desc: 'Virtual table running on the sqlite-vec extension. Performs fast cosine similarity lookups for FAISS.',
      sql: `CREATE VIRTUAL TABLE chunk_embeddings USING vec0(
    chunk_id TEXT PRIMARY KEY,
    embedding FLOAT[384] distance_metric=cosine
);`,
      indexes: [
        '-- Auto-indexed: Managed natively by the sqlite-vec extension block.'
      ]
    }
  };

  // SQL syntax highlighter (very simple client-side parser)
  function highlightSql(sql) {
    return sql
      .replace(/(--.*)/g, '<span class="sql-comment">$1</span>')
      .replace(/\b(CREATE TABLE|CREATE VIRTUAL TABLE|CREATE INDEX|PRIMARY KEY|REFERENCES|ON DELETE|DEFAULT|NOT NULL|ON|ON DELETE CASCADE|ON DELETE SET NULL|UNIQUE|CHECK|USING)\b/g, '<span class="sql-keyword">$1</span>')
      .replace(/\b(TEXT|INTEGER|REAL|FLOAT|vec0)\b/g, '<span class="sql-type">$1</span>');
  }

  function selectDatabaseTable(tableKey) {
    const data = schemasData[tableKey];
    if (!data) return;

    dbTableButtons.forEach(btn => {
      btn.classList.remove('active');
      if (btn.getAttribute('data-table') === tableKey) {
        btn.classList.add('active');
      }
    });

    dbSchemaTitle.textContent = data.title;
    dbSchemaDescription.textContent = data.desc;
    dbSchemaSql.innerHTML = highlightSql(data.sql);

    let indexesHtml = '';
    data.indexes.forEach(idx => {
      indexesHtml += `<li class="index-item">${idx}</li>`;
    });
    dbIndexesList.innerHTML = indexesHtml;
  }

  dbTableButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      selectDatabaseTable(btn.getAttribute('data-table'));
    });
  });

  // Initial database table selection
  selectDatabaseTable('documents');


  // ── AI Memory JSON Viewer ──────────────────────────────────────────────
  const memoryTabButtons = document.querySelectorAll('.tab-btn');
  const memoryJsonView = document.getElementById('memoryJsonView');
  const memoryDesc = document.getElementById('memoryDesc');

  const memoryData = {
    'concept': {
      desc: 'Tracks when specific concepts are encountered across documents, mapping user corrections, mastery levels, and recently formulated follow-up questions.',
      json: {
        "concept_id": "quantum-tunneling",
        "documents": [
          "doc-physics-intro-uuid", 
          "doc-semiconductors-uuid"
        ],
        "times_encountered": 3,
        "user_corrections": [
          {
            "original": "quantum tunneling is primarily used in standard silicon transistors",
            "corrected": "quantum tunneling is critical in tunnel diodes, flash memory leakage, and STM",
            "source": "user-chat-correction",
            "timestamp": "2026-07-05T14:22:00Z"
          }
        ],
        "mastery": 0.82,
        "last_reviewed": "2026-07-06T18:30:00Z",
        "related_questions_asked": [
          "How does wave function amplitude decay inside the barrier?",
          "What governs the tunneling probability?"
        ]
      }
    },
    'preference': {
      desc: 'Stores the stylistic output properties parsed from user settings or learned through interactive chat corrections.',
      json: {
        "preferred_note_style": "detailed_with_derivations",
        "preferred_flashcard_type": "cloze",
        "preferred_quiz_difficulty": "medium",
        "preferred_explanation_level": "intermediate",
        "default_export_format": "markdown",
        "theme": "dark",
        "reading_mode": "serif",
        "language": "en",
        "enable_diagrams": true,
        "enable_timeline": true
      }
    },
    'progress': {
      desc: 'Accumulates learning statistics, mastery metrics, weak topics, and active recall records categorized by topic clusters.',
      json: {
        "topics": {
          "quantum-mechanics": {
            "mastery": 0.75,
            "cards_reviewed": 45,
            "quiz_avg_score": 0.82,
            "time_spent_minutes": 240,
            "weak_areas": [
              "measurement-theory", 
              "quantum-entanglement"
            ],
            "strong_areas": [
              "wave-function-collapse", 
              "schrodinger-equation-derivation"
            ]
          },
          "neural-networks": {
            "mastery": 0.60,
            "cards_reviewed": 30,
            "quiz_avg_score": 0.70,
            "time_spent_minutes": 180,
            "weak_areas": [
              "backpropagation-partial-derivatives", 
              "attention-weight-scaling"
            ],
            "strong_areas": [
              "multilayer-perceptrons", 
              "activation-functions-sigmoid"
            ]
          }
        }
      }
    },
    'interaction': {
      desc: 'Keeps a localized sliding window history of recent queries, terms, and document traversal schedules to provide RAG context.',
      json: {
        "recent_chats": [
          {
            "query": "Derive backpropagation equations",
            "response_summary": "Explained chain rule dependencies and weight updates",
            "timestamp": "2026-07-07T08:15:20Z"
          }
        ],
        "last_ten_searches": [
          "backpropagation derivatives", 
          "MiniLM embedding dimensions", 
          "FAISS indexes"
        ],
        "document_interaction_order": [
          "doc-neural-networks", 
          "doc-embeddings"
        ],
        "frequently_accessed_concepts": [
          "gradient-descent", 
          "sentence-transformer"
        ]
      }
    },
    'correction': {
      desc: 'Logs direct overrides inputted by the user to overwrite default knowledge base parameters. The orchestrator references this before generating explanations.',
      json: {
        "corrections": [
          {
            "id": "corr-001",
            "original_ai_output": "Backpropagation was first developed in 2010 during the deep learning boom.",
            "user_correction": "Backpropagation was first introduced by Werbos in 1974, and popularized in 1986 by Rumelhart, Hinton, and Williams.",
            "context_document": "doc-neural-networks",
            "applied_to_future": true,
            "generalized": true
          }
        ]
      }
    }
  };

  // JSON syntax highlighter
  function highlightJson(jsonObj) {
    const jsonStr = JSON.stringify(jsonObj, null, 2);
    return jsonStr.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g, function (match) {
      let cls = 'json-number';
      if (/^"/.test(match)) {
        if (/:$/.test(match)) {
          cls = 'json-key';
        } else {
          cls = 'json-string';
        }
      } else if (/true|false/.test(match)) {
        cls = 'json-boolean';
      } else if (/null/.test(match)) {
        cls = 'json-null';
      }
      return '<span class="' + cls + '">' + match + '</span>';
    });
  }

  function selectMemoryTab(tabKey) {
    const data = memoryData[tabKey];
    if (!data) return;

    memoryTabButtons.forEach(btn => {
      btn.classList.remove('active');
      if (btn.getAttribute('data-tab') === tabKey) {
        btn.classList.add('active');
      }
    });

    memoryJsonView.innerHTML = highlightJson(data.json);
    memoryDesc.innerHTML = `<p style="font-weight: 500; line-height: 1.5;">${data.desc}</p>`;
  }

  memoryTabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      selectMemoryTab(btn.getAttribute('data-tab'));
    });
  });

  // Initial tab load
  selectMemoryTab('concept');


  // ── Documentation Content Search ──────────────────────────────────────
  const searchInput = document.getElementById('searchInput');
  
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      
      if (query === '') {
        // Remove highlighting and show all
        document.querySelectorAll('.searchable-content').forEach(el => {
          el.style.display = '';
        });
        return;
      }

      document.querySelectorAll('.searchable-content').forEach(el => {
        const text = el.innerText.toLowerCase();
        if (text.includes(query)) {
          el.style.display = '';
        } else {
          el.style.display = 'none';
        }
      });
    });
  }
});
