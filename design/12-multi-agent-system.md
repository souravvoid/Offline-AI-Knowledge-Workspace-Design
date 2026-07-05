# Multi-Agent AI System

## Architecture: Specialized Agent Pipeline

Khoji uses a **multi-agent system** where specialized models handle specific tasks, coordinated by an orchestrator. This is fundamentally different from using one LLM for everything.

```
┌─────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                            │
│  Routes work to specialized agents, merges results,         │
│  manages state, handles errors, tracks progress             │
└──────────┬──────────┬──────────┬──────────┬────────────────┘
           │          │          │          │
     ┌─────▼──┐ ┌────▼───┐ ┌───▼────┐ ┌──▼────────┐
     │ Agent 1│ │Agent 2 │ │Agent 3 │ │Agent N    │
     │        │ │        │ │        │ │           │
     │ OCR    │ │Layout  │ │Vision  │ │Knowledge  │
     │        │ │        │ │        │ │Extraction │
     └────────┘ └────────┘ └────────┘ └───────────┘
```

---

## Agent Specifications

### Agent 1: OCR Agent

**Model:** Tesseract v5 / EasyOCR / Surya OCR
**Fallback:** PaddleOCR

**Input:** PDF pages, images (PNG, JPG, WEBP)
**Output:** Extracted text with bounding boxes and confidence scores

**Responsibilities:**
- Detect text regions in scanned documents
- Recognize printed text in multiple languages
- Handle tables, multi-column layouts
- Provide confidence scores per word/line
- Fallback to alternative OCR engines on low confidence

**Performance Targets:**
- 10 pages/sec (Tesseract, CPU)
- 3 pages/sec (EasyOCR, CPU)
- 50 pages/sec (Tesseract, GPU)

### Agent 2: Layout Analysis Agent

**Model:** LayoutLMv3 / Detectron2
**Fallback:** Rule-based heuristic

**Input:** PDF page images + raw text
**Output:** Structured regions (title, paragraph, table, figure, formula, header, footer, page number)

**Responsibilities:**
- Identify document structure (title, sections, paragraphs)
- Detect tables and extract tabular data
- Identify figures, diagrams, and their captions
- Separate headers/footers from body text
- Detect formulas and equations
- Determine reading order within pages

**Output Format:**
```json
{
  "pages": [
    {
      "page_number": 1,
      "regions": [
        {"type": "title", "bbox": [10, 10, 600, 80], "text": "Chapter 1: Introduction"},
        {"type": "paragraph", "bbox": [10, 90, 600, 200], "text": "..."},
        {"type": "figure", "bbox": [10, 210, 300, 400], "caption": "Fig 1.1: ..."},
        {"type": "table", "bbox": [320, 210, 600, 400], "data": [[...]]},
        {"type": "formula", "bbox": [10, 410, 600, 450], "latex": "E=mc^2"},
      ]
    }
  ]
}
```

### Agent 3: Vision Agent

**Model:** Florence-2 / Qwen-VL (local vision model)
**Fallback:** None (skips if unavailable)

**Input:** Document images (figures, diagrams, charts, graphs)
**Output:** Text descriptions, data extracted from visual elements

**Responsibilities:**
- Describe figures and diagrams in text
- Extract data from charts and graphs
- Read text from complex diagrams (flowcharts, mind maps)
- Identify labeled parts in anatomical/technical diagrams
- Convert graph axes and data points to structured data

**Use Cases:**
- "Figure 1 shows a bar chart of GDP growth from 2010-2020..."
- "The circuit diagram shows an operational amplifier with feedback loop..."
- "The anatomical diagram labels the following parts: ..."

### Agent 4: Knowledge Extraction Agent

**Model:** Llama 3.2 1B / Phi-3 Mini (fine-tuned for extraction)
**Fallback:** Smaller extraction model

**Input:** Structured text (from Agents 1-3)
**Output:** Knowledge graph nodes and edges, key concepts, definitions, relationships

**Responsibilities:**
- Extract key concepts (entities, terms, definitions)
- Identify relationships between concepts (is-a, has-a, causes, depends-on, contradicts)
- Extract named entities (people, places, dates, formulas, equations)
- Identify hierarchical structure (parent concepts, sub-concepts)
- Detect claims, evidence, and conclusions
- Extract code snippets, algorithms, and procedures

**Output:**
```json
{
  "concepts": [
    {"id": "quantum-superposition", "name": "Quantum Superposition", "type": "principle"},
    {"id": "schrodinger-equation", "name": "Schrödinger Equation", "type": "formula"},
  ],
  "relationships": [
    {"source": "wave-particle-duality", "target": "quantum-superposition", "type": "foundation"},
    {"source": "schrodinger-equation", "target": "wave-function", "type": "governs"},
  ],
  "definitions": [
    {"term": "Superposition", "definition": "..."},
  ]
}
```

### Agent 5: Reasoning Agent

**Model:** Llama 3.2 1B / Phi-3 Mini
**Fallback:** Smaller reasoning model

**Input:** Extracted concepts + relationships + raw text
**Output:** Summary, explanations, analogies, important questions

**Responsibilities:**
- Generate multi-level summaries (TL;DR, detailed, technical)
- Create explanations at different complexity levels (beginner, intermediate, expert)
- Generate analogies and examples
- Identify important questions for comprehension checking
- Extract cause-effect chains
- Identify arguments and counter-arguments
- Generate learning objectives

**Output:**
```markdown
## TL;DR
Quantum mechanics describes nature at atomic scales...

## Beginner Explanation
Imagine you're playing a game where a coin is spinning...

## Expert Explanation
The Hilbert space formulation provides...

## Important Questions
1. How does wave-particle duality challenge classical intuition?
2. What experimental evidence supports quantum superposition?
```

### Agent 6: Knowledge Graph Agent

**Model:** Graph processing (algorithmic, not ML)
**Fallback:** N/A

**Input:** Concepts + relationships from Agent 4
**Output:** Interactive knowledge graph data, merged with existing graph

**Responsibilities:**
- Merge new concepts into existing knowledge graph
- Detect cross-document connections (same concept in different documents)
- Discover implicit relationships (transitive, shared properties)
- Compute concept centrality and importance
- Generate learning paths (prerequisite → dependent concept ordering)
- Cluster related concepts into topics
- Auto-generate backlinks between documents

**Algorithm:**
```
1. Extract concepts C_new from document D
2. For each c in C_new:
   a. Find matching concepts in existing graph (by name, embedding similarity)
   b. If match found, merge (add relationships, increment reference count)
   c. If no match, add as new node
3. For all relationships R_new:
   a. Add to graph
   b. Check transitive closure for implicit connections
4. Recompute centrality scores
5. Identify concept clusters (community detection)
6. Generate learning path suggestions
```

### Agent 7: Flashcard Agent

**Model:** Llama 3.2 1B (fine-tuned for card generation)
**Fallback:** Rule-based extraction

**Input:** Key concepts, definitions, relationships
**Output:** Anki-compatible flashcards (cloze deletion + Q&A)

**Responsibilities:**
- Generate cloze deletion cards from definitions
- Generate Q&A cards from concept pairs
- Generate "which of these" concept discrimination cards
- Generate image occlusion cards from diagrams
- Tag cards by topic, difficulty, and document source
- Avoid duplicate cards across documents
- Generate distractors for multiple-choice cards

**Card Types:**
```
Type 1: Cloze Deletion (fill in the blank)
  "The {{c1::Heisenberg Uncertainty Principle}} states that..."

Type 2: Q&A
  Q: "What is the relationship between wave functions and probability density?"
  A: "The probability density is |Ψ|², the square of the wave function magnitude."

Type 3: Concept Discrimination
  "Which is NOT a quantum mechanical principle? (A) Superposition (B) Uncertainty (C) Entropy"

Type 4: Image Occlusion (for diagrams)
  [Diagram with labeled parts hidden]
```

### Agent 8: Quiz Agent

**Model:** Llama 3.2 1B
**Fallback:** Smaller model

**Input:** Extracted concepts, raw text
**Output:** Multiple-choice questions with distractors

**Responsibilities:**
- Generate MCQs at configurable difficulty levels
- Generate true/false questions
- Generate fill-in-the-blank questions
- Generate matching questions (pair concepts)
- Generate ordering questions (timeline events)
- Distractors are semantically plausible but incorrect
- Tag questions by topic and difficulty
- Avoid duplicate questions across quiz generations

### Agent 9: Diagram Agent

**Model:** Code generation (fine-tuned for Mermaid syntax)
**Fallback:** Template-based generation

**Input:** Concepts, relationships, hierarchical structure, timeline data
**Output:** Mermaid diagram code (flowchart, mindmap, timeline, ER, sequence, class)

**Responsibilities:**
- Generate flowcharts for processes and workflows
- Generate mind maps for concept hierarchies
- Generate timelines for chronological events
- Generate ER diagrams for entity relationships
- Generate sequence diagrams for processes and protocols
- Generate class diagrams for taxonomies
- Generate decision trees for classification/choice
- Ensure diagrams are visually clean (not overly complex)

### Agent 10: Markdown Agent

**Model:** Llama 3.2 1B
**Fallback:** Template-based formatting

**Input:** All outputs from Agents 1-9
**Output:** Structured Markdown document

**Responsibilities:**
- Assemble all outputs into a coherent Markdown document
- Apply consistent formatting (headings, lists, code blocks, tables)
- Insert diagrams at appropriate locations
- Add cross-references and backlinks
- Generate YAML frontmatter (metadata, tags, source info)
- Ensure proper heading hierarchy
- Output: `document-name.md` with complete notes

### Agent 11: Review & Spaced Repetition Agent

**Model:** Algorithmic (SM-2/FSRS algorithm)
**Fallback:** N/A

**Input:** Flashcard review history, user ratings
**Output:** Review queue, scheduling, statistics

**Responsibilities:**
- Implement SM-2 or FSRS spaced repetition algorithm
- Schedule card reviews based on difficulty and history
- Track retention statistics per card, per topic, per document
- Identify weak topics (low retention clusters)
- Prioritize cards for review
- Generate review sessions (optimal order)
- Export review data for Anki compatibility

### Agent 12: Export Agent

**Model:** Template renderer
**Fallback:** N/A

**Input:** All generated content
**Output:** Exported files in user-selected format

**Supported Formats:**
- Markdown (with frontmatter)
- Anki .apkg package
- PDF with formatting
- LaTeX document
- JSON structured data
- CSV (flashcards, quiz)
- Plain text
- HTML (self-contained)

---

## Agent Coordination

```
                    ┌──────────────────┐
                    │  Orchestrator    │
                    │  (Rust/Tauri)    │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
   │ Agent 1 │ ◄─────► │ Agent 2 │ ◄─────► │ Agent 3 │
   │  OCR    │   dep    │ Layout │   dep    │ Vision  │
   └────┬────┘         └────┬────┘         └────┬────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                     ┌──────▼──────┐
                     │   Agent 4   │
                     │  Knowledge  │
                     │  Extraction │
                     └──────┬──────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
         ┌────▼───┐   ┌────▼───┐   ┌────▼────┐
         │ Agent 5│   │ Agent 6│   │ Agent 7 │
         │Reason  │   │KG Graph│   │Flashcard│
         └────┬───┘   └────────┘   └────┬────┘
              │                         │
         ┌────▼───┐               ┌────▼────┐
         │ Agent 8│               │ Agent 11│
         │ Quiz   │               │ Review  │
         └────┬───┘               │(SR)     │
              │                   └─────────┘
         ┌────▼───┐
         │ Agent 9│
         │Diagram │
         └────┬───┘
              │
         ┌────▼───┐
         │ Agent 10│
         │Markdown │
         └────┬───┘
              │
         ┌────▼───┐
         │ Agent 12│
         │ Export  │
         └────────┘
```

## Agent Communication Protocol

Agents communicate through a structured message bus:

```json
{
  "job_id": "uuid-1234",
  "agent": "knowledge-extraction",
  "input": {
    "text": "...",
    "layout": {...},
    "config": {"model": "llama-3.2-1b", "language": "en"}
  },
  "output": {...},
  "status": "completed",
  "error": null,
  "performance": {"duration_ms": 2450, "tokens_used": 1200}
}
```

## Model Selection Strategy

| Agent | Small (4GB RAM) | Medium (8GB RAM) | Large (16GB+ RAM) |
|-------|-----------------|------------------|-------------------|
| OCR | Tesseract v5 | EasyOCR | Surya OCR |
| Layout | Heuristic | LayoutLMv3 | LayoutLMv3 |
| Vision | None (skip) | Florence-2 (base) | Florence-2 (large) |
| Knowledge | Llama 3.2 1B | Phi-3 Mini 3.8B | Mistral 7B |
| Reasoning | Llama 3.2 1B | Phi-3 Mini 3.8B | Mistral 7B |
| Flashcard | Llama 3.2 1B | Phi-3 Mini 3.8B | Mistral 7B |
| Quiz | Llama 3.2 1B | Phi-3 Mini 3.8B | Mistral 7B |
| Diagram | Template | Template + LLM | LLM only |
| Markdown | Template | Template + LLM | LLM only |
| Embedding | All-MiniLM-L6-v2 | All-MiniLM-L6-v2 | BGE-Large |
