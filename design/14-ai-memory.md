# AI Memory System

## Overview

Khoji's AI has persistent memory across sessions. It remembers what you've learned, corrected, preferred, and struggled with. All memory is stored **locally** in the SQLite database — nothing leaves the device.

## Memory Types

### 1. Concept Memory

The AI remembers every concept it has extracted and how concepts connect across documents.

```json
{
  "concept_id": "quantum-tunneling",
  "documents": ["doc-physics", "doc-semiconductors"],
  "times_encountered": 3,
  "user_corrections": [
    {"original": "quantum tunneling used in transistors", "corrected": "quantum tunneling used in tunnel diodes and flash memory", "source": "user-chat-correction", "timestamp": "..."}
  ],
  "mastery": 0.8,
  "last_reviewed": "2026-07-02",
  "related_questions_asked": ["How does tunneling relate to band gaps?", "What is the tunneling probability formula?"]
}
```

### 2. Preference Memory

The AI remembers user preferences for output style, detail level, and format.

```json
{
  "preferred_note_style": "detailed",
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
```

### 3. Progress Memory

The AI tracks learning progress across topics.

```json
{
  "topics": {
    "quantum-mechanics": {
      "mastery": 0.75,
      "cards_reviewed": 45,
      "quiz_avg_score": 0.82,
      "time_spent_minutes": 240,
      "weak_areas": ["measurement-theory", "quantum-entanglement"],
      "strong_areas": ["wave-function", "schrodinger-equation"]
    },
    "neural-networks": {
      "mastery": 0.6,
      "cards_reviewed": 30,
      "quiz_avg_score": 0.7,
      "time_spent_minutes": 180,
      "weak_areas": ["backpropagation-math", "attention-mechanisms"],
      "strong_areas": ["perceptron", "activation-functions"]
    }
  }
}
```

### 4. Interaction Memory

The AI remembers recent interactions for context.

```json
{
  "recent_chats": [
    {"query": "Explain backpropagation", "response_summary": "...", "timestamp": "..."},
    {"query": "Generate more quiz questions", "response_summary": "...", "timestamp": "..."}
  ],
  "last_ten_searches": ["backpropagation", "neural network types", "loss functions"],
  "document_interaction_order": ["doc-ml", "doc-deep-learning", "doc-transformers"],
  "frequently_accessed_concepts": ["gradient-descent", "activation-function", "loss-function"]
}
```

### 5. Correction Memory

When a user corrects the AI, it remembers and adapts.

```json
{
  "corrections": [
    {
      "id": "corr-001",
      "original_ai_output": "Backpropagation was invented in 2010",
      "user_correction": "Backpropagation was popularized in 1986 by Rumelhart, Hinton, and Williams",
      "context_document": "doc-neural-networks",
      "applied_to_future": true,
      "generalized": true
    }
  ]
}
```

## AI Memory UI

### Memory Dashboard

```
┌────────────────────────────────────────────────────────────┐
│ 🧠 AI Memory & Progress                         [⚙️ Manage]│
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Learning Progress by Topic                                 │
│ ─────────────────────────────────────────────────────       │
│                                                            │
│ Quantum Mechanics      ████████░░░░░░  75%  ⚡ Review due │
│ Neural Networks        ██████░░░░░░░░  60%                 │
│ Organic Chemistry      ████░░░░░░░░░░  40%  🆕 New        │
│ Algorithms             ██████████░░░░  85%  📊 Strong     │
│                                                            │
│ Recent Corrections (2)                                     │
│ ┌─── Backpropagation date ──────────────────────────────┐  │
│ │ You corrected: "Invented 2010" → "Published 1986"     │  │
│ │ AI has applied this correction in 3 subsequent chats. │  │
│ └───────────────────────────────────────────────────────┘  │
│                                                            │
│ AI Knows About You:                                        │
│ • You prefer detailed explanations with examples           │
│ • You like cloze-deletion flashcards over Q&A              │
│ • You struggle with measurement theory in QM               │
│ • You've corrected the AI 2 times (both applied)          │
│ • You study most actively between 8-11 PM                  │
│                                                            │
│ [Clear Memory] [Export Memory] [Reset Topic Progress]      │
└────────────────────────────────────────────────────────────┘
```

## How Memory Affects AI Behavior

### Chat Responses

Without Memory:
> User: "Explain backpropagation"
> AI: "Backpropagation is an algorithm..." (generic)

With Memory:
> User: "Explain backpropagation"
> AI: "Backpropagation computes gradients using the chain rule."
> "I notice you had questions about the math last time. Let's go through the derivation step by step with an example." (adapts to user's known weakness)

### Flashcard Generation

Without Memory:
> Generates: 10 random cards at default difficulty

With Memory:
> Generates: 5 review cards for weak areas + 5 new cards
> Prioritizes concepts user got wrong in last quiz
> Uses cloze format (user's preference)

### Quiz Generation

Without Memory:
> Generates: 10 random questions

With Memory:
> Generates: 7 questions on weak topics + 3 on strong topics
> Difficulty calibrated to user's historical performance (80% target)
> Skips topics user has mastered

### Summary Generation

Without Memory:
> One summary, fixed format

With Memory:
> User prefers detailed summaries → includes derivations
> User has strong background in math → skips basic math, goes to advanced
> User prefers analogies → includes 2-3 analogies per concept

## Privacy & Memory Control

The user has full control over AI memory:

| Control | Description |
|---------|-------------|
| **View Memory** | See everything AI knows about you |
| **Edit Memory** | Correct or delete specific memories |
| **Clear Memory** | Reset all memory (fresh start) |
| **Selective Forget** | "Forget everything about quantum mechanics" |
| **Export Memory** | Download memory as JSON |
| **Pause Memory** | Temporarily disable memory updates |
| **Memory Scope** | Per-document vs global memory |
| **Sync Memory** | Optional: sync across devices (LAN/local network) |

## Memory Storage

```
~/.khoji/db/khoji.db
├── memory_concepts        → Concept memory table
├── memory_preferences     → User preference table
├── memory_progress        → Topic progress table
├── memory_interactions    → Recent interaction log
├── memory_corrections     → User correction log
└── memory_embeddings      → Concept embedding vectors (for similarity search)
```

Storage estimate: ~5MB per 100 documents with full memory history.
