# Interactive Knowledge Graph

## Overview

The Knowledge Graph is the beating heart of Khoji. Unlike traditional note-taking apps where each document is an island, Khoji extracts concepts from every document and merges them into a unified, interactive graph.

```
Document A: Intro to ML           Document B: Neural Networks
─────────────────────────         ─────────────────────────
├── Supervised Learning           ├── Perceptron
├── Unsupervised Learning         ├── Backpropagation
├── Overfitting                   ├── Activation Functions
├── Train/Test Split              ├── Gradient Descent
└── Cross-Validation              └── Loss Functions

                ┌─────────────────────────────────┐
                │         KNOWLEDGE GRAPH          │
                │                                   │
                │  Supervised Learning ─────┐       │
                │       │                  │        │
                │       ├── Train/Test     │        │
                │       │   Split          │        │
                │       │                  │        │
                │       ├── Cross-         │        │
                │       │   Validation     │        │
                │       │                  │        │
                │       └── Overfitting ───┼── Neural│
                │                         │   Networks│
                │  Unsupervised Learning  │       │   │
                │       │                 │  ┌────┘   │
                │       └── Clustering    │  │        │
                │                         │  ▼        │
                │                    Backpropagation  │
                │                         │          │
                │                    Gradient Descent │
                └─────────────────────────────────────┘
```

## Graph Data Model

```json
{
  "nodes": [
    {
      "id": "backpropagation",
      "name": "Backpropagation",
      "type": "algorithm",
      "description": "Algorithm for training neural networks...",
      "documents": ["doc-neural-networks", "doc-deep-learning"],
      "tags": ["machine-learning", "neural-networks", "training"],
      "confidence": 0.95,
      "created": "2026-07-03",
      "page_refs": [{"doc": "neural-networks.pdf", "page": 42}]
    }
  ],
  "edges": [
    {
      "source": "backpropagation",
      "target": "gradient-descent",
      "relationship": "uses",
      "strength": 0.9,
      "bidirectional": false
    }
  ]
}
```

## Graph Visualization Features

### 1. Interactive Canvas

```
┌───────────────────────────────────────────────────────────────┐
│  Knowledge Graph: ML Basics                    [🔍 ⚙️ ⟲]      │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│              ┌──────────────┐                                 │
│              │  Supervised  │──────┐                          │
│              │  Learning    │      │                          │
│              └──────┬───────┘      │                          │
│                     │              │                          │
│           ┌─────────┼─────────┐    │    ┌──────────────┐     │
│           │         │         │    └────│  Neural       │     │
│     ┌─────▼──┐ ┌────▼───┐ ┌───▼───┐   │  Networks     │     │
│     │ Train  │ │ Cross  │ │ Over- │   └──────┬───────┘     │
│     │ /Test  │ │ Valid. │ │fitting│          │              │
│     └────────┘ └────────┘ └───────┘          │              │
│                                        ┌──────┴──────┐      │
│                              ┌─────────┤Backpropaga- │      │
│                              │         │tion         │      │
│                              │         └──────┬──────┘      │
│                              │                │             │
│                         ┌────▼───┐     ┌──────▼──────┐      │
│                         │Gradient│     │  Activation  │      │
│                         │Descent │     │  Functions   │      │
│                         └────────┘     └─────────────┘      │
│                                                               │
│  [⟲ Reset View] [🔍 Fit] [+][-] [◉ Force Layout] [🎯 Center] │
│  Selected: Backpropagation | 2 documents | 4 connections     │
└───────────────────────────────────────────────────────────────┘
```

### 2. Interaction Design

| Interaction | Behavior |
|-------------|----------|
| **Click node** | Select concept → show details panel |
| **Double-click node** | Open source document at relevant page |
| **Drag node** | Reposition (temporarily override layout) |
| **Hover node** | Highlight connected nodes, dim rest |
| **Hover edge** | Show relationship type label |
| **Scroll** | Zoom in/out |
| **Drag background** | Pan canvas |
| **Pinch (touch)** | Zoom |
| **Cmd+Click** | Multi-select |
| **Right-click node** | Context menu: Open doc, Generate flashcards, Chat about this |
| **Search bar** | Filter graph to matching nodes |
| **Lasso select** | Select multiple nodes (for grouping) |

### 3. Node Types & Visual Encoding

| Concept Type | Icon | Color | Shape | Border |
|-------------|------|-------|-------|--------|
| Core Principle | ⚛️ | Primary (indigo) | Circle | Thick |
| Formula | ∑ | Accent (violet) | Diamond | — |
| Algorithm | ⚙️ | Secondary (sky) | Rounded rect | — |
| Definition | 📖 | Neutral | Circle | Thin |
| Person | 👤 | Green | Circle | — |
| Date/Event | 📅 | Amber | Rectangle | — |
| Dataset | 📊 | Emerald | Rounded rect | Dashed |
| Tool/Framework | 🔧 | Rose | Rounded rect | — |
| Code Concept | 💻 | Cyan | Monospace rect | — |
| Question | ❓ | Orange | Diamond | Dashed |
| User Note | 📝 | Surface card | Rect | User-specified |
| Document | 📄 | Neutral | Large rect | Thick |

### 4. Layout Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **Force-directed** | Default — good for general concept relationships |
| **Hierarchical** | Taxonomy, prerequisites, learning paths |
| **Radial** | Single concept with many related sub-concepts |
| **Timeline** | Chronological ordering of events/discoveries |
| **Cluster** | Group related topics into colored clusters |
| **Grid** | Large number of similar-type nodes |

### 5. Detail Panel

When a node is selected, a slide-over panel appears:

```
┌────────────────────────────────────────────────────────────┐
│ ◼ Backpropagation                               [✕]       │
├────────────────────────────────────────────────────────────┤
│ Algorithm · #neural-networks #training #deep-learning      │
│                                                            │
│ Description:                                                │
│ Backpropagation computes the gradient of the loss          │
│ function with respect to the weights of a neural           │
│ network by applying the chain rule from calculus.          │
│                                                            │
│ Source Documents:                                           │
│ ┌─── 📄 Deep Learning (p.42) ──────────────────────────┐  │
│ │  "The backpropagation algorithm computes gradients..." │  │
│ └───────────────────────────────────────────────────────┘  │
│ ┌─── 📄 Neural Networks (p.89) ─────────────────────────┐  │
│ │  "We use backpropagation to train multi-layer..."      │  │
│ └───────────────────────────────────────────────────────┘  │
│                                                            │
│ Connections (4):                                           │
│  ▶︎ Uses: Gradient Descent                                 │
│  ▶︎ Used by: Neural Network Training                       │
│  ▶︎ Requires: Chain Rule                                   │
│  ▶︎ Related to: Automatic Differentiation                  │
│                                                            │
│ Actions:                                                    │
│ [📝 View Notes] [🃏 Generate Cards] [💬 Ask AI] [📤 Export]│
│                                                            │
│ Learning Status: [████████░░] 80% Mastered                  │
│ Last reviewed: 2 days ago                                   │
└────────────────────────────────────────────────────────────┘
```

### 6. Cross-Document Connections

The knowledge graph automatically discovers connections between documents:

```
Document 1: "Quantum Mechanics"          Document 2: "Semiconductor Physics"
─────────────────────────────           ─────────────────────────────────
├── Wave Function                       ├── Energy Bands
├── Schrödinger Equation                ├── Band Gap
├── Uncertainty Principle               ├── Electron Holes
└── Quantum Tunneling ──────────────────┼── Quantum Tunneling (same concept!)
                                        └── Doping

Result in Knowledge Graph:
  "Quantum Tunneling" node now references BOTH documents.
  Edge added: "Quantum Tunneling" ← "related to" → "Band Gap"
```

### 7. Auto-Generated Backlinks

Every concept node automatically generates backlinks in the Markdown notes:

```markdown
## Quantum Tunneling

Quantum tunneling is a phenomenon where a particle passes through
a potential barrier that it classically could not surmount.

**See also:**
- [[Semiconductor Physics/Energy Bands]] — Tunneling in semiconductors
- [[Quantum Mechanics/Wave Function]] — Mathematical foundation
- [[Semiconductor Physics/Quantum Tunneling]] — (same concept in other doc)
```

### 8. Learning Path Generation

The Knowledge Graph Agent can generate optimal learning paths:

```
Concept: Transformers (ML)
┌─────────────────────────────────────────────────────────┐
│ Recommended Learning Path:                               │
│                                                         │
│ 1. [✓] Neural Networks Basics         ── doc1.pdf       │
│ 2. [✓] Backpropagation                ── doc1.pdf       │
│ 3. [✓] Word Embeddings                ── doc3.pdf       │
│ 4. [  ] Sequence Models (RNN/LSTM)    ── doc4.pdf       │
│ 5. [  ] Attention Mechanism           ── doc5.pdf       │
│ 6. [  ] Transformer Architecture      ── current        │
│ 7. [  ] BERT/GPT Variants             ── doc6.pdf       │
│                                                         │
│ Prerequisites missing: Self-Attention (doc5.pdf, p.12)  │
│ Recommended: Review doc5.pdf before continuing.          │
└─────────────────────────────────────────────────────────┘
```
