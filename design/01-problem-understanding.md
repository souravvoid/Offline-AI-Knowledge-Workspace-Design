# Phase 1: Problem Understanding & User Research

## Product Name: **Khoji** (खोजी — "The Seeker")

A Sanskrit-derived name meaning "one who searches, explores, discovers." The knowledge operating system.

---

## Vision: The VS Code for Knowledge

**Khoji is not a document summarizer. It is a local-first AI operating system that transforms documents into a permanent, interconnected knowledge graph.**

Every imported document becomes part of a growing knowledge base that the AI continuously understands, links, and enriches over time. Unlike tools that produce isolated notes, Khoji builds a living second brain:

```
Document → Concepts → Connections → Knowledge Graph → Growing Intelligence
```

## Product Principles

| Principle | Meaning |
|-----------|---------|
| **Privacy First** | Zero data leaves the device. Ever. |
| **Local First** | No cloud dependency. Works on a plane, in a basement, anywhere. |
| **Markdown First** | All knowledge is plain Markdown. Portable. Version-controllable. Forever yours. |
| **AI Native** | AI is not a feature — it is the operating system of the knowledge workspace. |
| **Keyboard First** | Every action accessible via keyboard. VS Code-level efficiency. |
| **Open Source First** | Community extensible. No vendor lock-in. Your stack, your rules. |
| **Fast First** | UI in <16ms. Search in <50ms. Processing in seconds. |
| **Offline by Default** | Network is never assumed. Offline is the primary mode. |

---

## The Core Problem

Knowledge workers today interact with information across fragmented tools:

| Tool | Strength | Weakness |
|------|----------|----------|
| **PDF Readers** | Portable format | Read-only, no extraction |
| **Notion/Obsidian** | Great notes | Manual entry, no AI |
| **ChatGPT** | Smart answers | No memory, no structure, no offline |
| **NotebookLM** | Google-grade AI | Cloud-only, no Markdown, Google lock-in |
| **Anki** | Spaced repetition | Manual card creation |
| **Mendeley/Zotero** | Reference management | Heavy, academic focus, no AI |
| **Obsidian + Local AI** | Local + Markdown | Complex setup, no document understanding, plugin fragmentation |

**The gap:** No single tool exists that:
- Runs **100% offline**
- Understands **any document** (PDF, image, PPT, DOCX, EPUB)
- Builds a **permanent, interconnected knowledge graph** over time
- Uses **specialized multi-agent AI** (not one generic model)
- Stores everything in **portable Markdown**
- Provides **AI memory** (remembers your corrections, preferences, progress)
- Has **plugin architecture** for extensibility
- Is **fast, minimal, and developer-friendly**
- Works on **4GB RAM devices** with **CPU-only**

## Target Users (High-Level)

1. **Engineering Students** — studying textbooks, research papers, technical documentation
2. **Medical Students** — dense anatomy/physiology texts, diagrams, reference materials
3. **Researchers** — reading papers, extracting citations, building literature reviews
4. **Software Engineers** — technical docs, API references, architecture decisions, learning new stacks
5. **Professors/Teachers** — preparing lectures, creating quizzes, organizing course materials
6. **Lifelong Learners** — continuous learning, personal knowledge management, second brain

## Pain Points (Validated)

1. **Knowledge Fragmentation** — Information scattered across PDFs, notes, bookmarks, chat history, and browser tabs
2. **Context Switching** — Students use 5+ apps to study one document
3. **Manual Work** — Creating flashcards and notes by hand is slow and error-prone
4. **Forgetting** — No spaced repetition built into reading workflow; Ebbinghaus curve is real
5. **Lock-in** — Cloud tools own your knowledge; export is limited or non-existent
6. **Search Sucks** — PDF search is primitive; no semantic understanding across documents
7. **One-size-fits-all** — Current tools don't adapt to how you learn (visual, reading, quiz-based)
8. **Setup Complexity** — Local AI tools require Python, CUDA, pip installs — too technical for most users
9. **No Cross-Document Understanding** — Tools treat each PDF in isolation; no knowledge graph across your library
10. **No AI Memory** — Current tools forget what you've learned, corrected, or preferred

## User Goals

| Goal | Priority |
|------|----------|
| Upload any document → permanent knowledge graph | P0 |
| Multi-agent AI that understands, connects, and teaches | P0 |
| Auto-generated flashcards with spaced repetition | P0 |
| Semantic search across entire knowledge base | P0 |
| Interactive knowledge graph with clickable concepts | P0 |
| AI memory (remembers corrections, preferences, progress) | P0 |
| Export to Markdown/Anki/PDF/LaTeX | P1 |
| Plugin architecture for extensibility | P1 |
| Fully offline operation | P0 |
| Fast startup (<3s), 4GB RAM compatible | P0 |
| Git synchronization | P2 |
| Mobile companion | P2 |

## Current Workflow (Broken)

```
Read PDF → Manually highlight → Copy to Obsidian → Create Anki cards → Search Google → Switch to ChatGPT → Copy answers back → Repeat for next PDF → No connections between documents
```

## Desired Workflow

```
Upload PDF → AI multi-agent pipeline → Knowledge graph integration → Notes + Flashcards + Quiz + Mind Map
→ AI memory updates → Cross-document connections → Review with spaced repetition → Chat with full context
→ Export → Knowledge base grows smarter with every document
```

## Competitive Advantages

1. **Knowledge OS, Not a Document Reader** — The product is a knowledge operating system that grows with you
2. **Multi-Agent AI** — Specialized agents (OCR, Layout, Knowledge Extraction, Reasoning, Diagram, Flashcard) working together, not one generic model
3. **Interactive Knowledge Graph** — Concepts are automatically extracted, linked, and visualized in a clickable graph
4. **AI Memory** — The system remembers your corrections, preferred writing style, weak topics, and study progress across sessions
5. **Truly Offline** — No internet needed for core AI features; privacy guaranteed
6. **Markdown-Native** — All knowledge is plain Markdown files; fork, merge, diff, version-control
7. **Plugin Architecture** — SDK for OCR, models, exporters, diagrams, citations, translations
8. **Low Resource** — Designed for 4GB RAM, CPU-only, integrated GPU

## Key Differentiators vs Competitors

| Capability | Khoji | NotebookLM | Obsidian | ChatGPT | Logseq |
|-----------|-------|------------|----------|---------|--------|
| Fully offline | ✅ | ❌ | ✅ | ❌ | ✅ |
| Markdown native | ✅ | ❌ | ✅ | ❌ | ✅ |
| Knowledge graph | ✅ Interactive | ❌ | ⚠️ Plugin | ❌ | ✅ |
| Multi-agent AI | ✅ | ❌ | ⚠️ Plugin | ⚠️ Single | ❌ |
| AI memory | ✅ | ❌ | ❌ | ⚠️ Session | ❌ |
| Document understanding | ✅ All formats | ⚠️ PDF/audio | ❌ | ⚠️ Limited | ❌ |
| Flashcards | ✅ With SR | ⚠️ Audio only | ⚠️ Plugin | ❌ | ❌ |
| Quiz generation | ✅ | ❌ | ❌ | ❌ | ❌ |
| Plugin ecosystem | ✅ Built-in SDK | ❌ | ✅ | ❌ | ⚠️ Limited |
| Privacy | ✅ 100% local | ❌ | ✅ | ❌ | ✅ |
| 4GB RAM support | ✅ | ❌ (cloud) | ✅ | ❌ (cloud) | ✅ |
| Spaced repetition | ✅ Built-in | ❌ | ⚠️ Plugin | ❌ | ⚠️ Plugin |

## Design Principles

1. **Knowledge First** — Every feature serves the goal of understanding, connecting, and retaining knowledge
2. **Invisible AI** — AI should feel like a natural part of the workflow, not a chatbot gimmick
3. **Filesystem Native** — Your knowledge lives as files you own, in a format you control
4. **Fast by Default** — Under 100ms for UI interactions, under 30s for document processing
5. **Progressive Disclosure** — Simple for beginners, powerful for experts
6. **Offline by Design** — Network is never assumed; offline is the primary, not fallback, mode
7. **Accessible to All** — Works for low-vision, keyboard-only, low-RAM users
8. **AI Should Never Just Summarize** — It should understand, reason, connect, organize, teach, visualize, and generate relationships

## AI Philosophy

The AI in Khoji follows these rules:

1. **Never merely summarize.** It must understand the structure of knowledge, not just rephrase text.
2. **Always reason.** Extract causal relationships, hierarchies, dependencies, and contradictions.
3. **Always connect.** Every new document links into the existing knowledge graph, creating backlinks and discovering relationships.
4. **Organize automatically.** Concepts are categorized, tagged, and clustered without user intervention.
5. **Teach, don't tell.** Generate explanations at multiple levels of complexity. Adapt to the user's demonstrated understanding.
6. **Visualize.** Every concept cluster should be representable as a diagram, graph, or map.
7. **Generate knowledge, not text.** The output is structured knowledge (notes, cards, graphs, relationships), not paragraphs.
