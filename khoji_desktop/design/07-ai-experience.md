# Phase 9-10: Animations & AI Experience

## Animation Principles

1. **Purposeful** — Every animation serves a function (feedback, focus, orientation)
2. **Fast** — Under 200ms for micro-interactions, under 500ms for transitions
3. **Subtle** — No gratuitous motion. Easing: cubic-bezier(0.4, 0, 0.2, 1)
4. **Responsive** — Respects `prefers-reduced-motion`
5. **Progressive** — Complex animations only on capable hardware

---

## Animation Specifications

### Micro-Interactions (<200ms)

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Button hover | Background color + shadow | 150ms | ease |
| Button click | Scale 0.97 | 100ms | ease-out |
| Card hover | Lift (translateY -2px) + shadow | 200ms | ease-out |
| Toggle switch | Knob slide + bg color | 200ms | spring |
| Checkbox | Checkmark draw | 150ms | ease |
| Input focus | Border color + ring | 200ms | ease |
| Icon spin (loading) | 360° rotation | 600ms | linear |
| Tooltip | Fade in + translateY(4→0) | 150ms | ease-out |

### Transitions (200-500ms)

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Sidebar collapse | Width + opacity | 250ms | ease-in-out |
| Tab switch | Content crossfade | 200ms | ease |
| Page transition | Slide (direction depends) | 300ms | ease-in-out |
| Modal open | Scale(0.95→1) + fade | 200ms | ease-out |
| Modal close | Scale(1→0.95) + fade | 150ms | ease-in |
| Dropdown open | Fade + translateY(-4→0) | 150ms | ease-out |
| Dropdown close | Fade + translateY(0→-4) | 100ms | ease-in |
| Flashcard flip | 3D rotateY(180°) | 400ms | ease-in-out |
| Quiz option select | Scale + bg color | 150ms | ease |

### Pipeline Animations (Sequential)

Each stage in the AI pipeline lights up with:
1. Current step: Pulsing glow + spinner
2. Completed step: Green checkmark + fade to dim
3. Next step: Subtle pulse (waiting)
4. Error: Red shake + exclamation

The pipeline bar uses a **progress snake** — a gradient that flows left-to-right.

### Upload Animation

```
1. Drag file over drop zone:
   - Border turns dashed, primary color
   - Subtle pulsing glow
   - "Drop to upload" text scales up

2. File accepted:
   - Drop zone shrinks to card
   - File icon appears with name
   - Green checkmark crosses in

3. Processing starts:
   - Pipeline visualization slides up
   - First step activates with pulse
```

### AI Thinking Animation

When the LLM is generating a response:
- Three dots bounce with staggered delay
- Small brain/sparkle icon rotates slowly
- "Thinking..." text fades in/out
- Duration adapts to actual generation time

Rather than a generic spinner, show **what the AI is doing**:
```
🤖 Reading document...    (loading context)
   ──> Analyzing query...  (processing)
   ──> Generating...       (token generation)
   ──> ✓ Done              (complete)
```

---

## AI Experience Design

### The AI Pipeline

```
User Uploads Document
        │
        ▼
┌───────────────────┐
│ 1. Preprocessing  │  ◀── Show: "Extracting text..."
│   • PDF parsing   │       Progress: indeterminate
│   • OCR (if image)│       Time: 1-30s
│   • Layout detect │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 2. Text Chunking  │  ◀── Show: "Processing text..."
│   • Sentence split│       Progress: chunk counter
│   • Semantic chunk│       Time: 2-10s
│   • Overlap 10%   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 3. Embeddings     │  ◀── Show: "Creating embeddings..."
│   • Local model   │       Progress: vector count
│   • 384-dim vecs  │       Time: 5-30s
│   • Store in DB   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ 4. LLM Processing │  ◀── Show: "AI analyzing..."
│   • Summarize     │       Progress: token counter
│   • Extract key   │       Time: 30-120s (1B model)
│   • Generate MD   │       Sub-steps shown as list
└─────────┬─────────┘
          │
          ├─────────────────────┐
          ▼                     ▼
┌───────────────────┐  ┌───────────────────┐
│ 5. Flashcard Gen  │  │ 6. Quiz Gen       │
│   • Cloze delete  │  │   • MCQ questions │
│   • Q&A pairs     │  │   • Distractors   │
│   • 10-50 cards   │  │   • 5-20 Qs       │
└─────────┬─────────┘  └─────────┬─────────┘
          │                      │
          ▼                      ▼
┌───────────────────┐  ┌───────────────────┐
│ 7. Mind Map Gen   │  │ 8. Export Prep    │
│   • Concept graph │  │   • Markdown      │
│   • Hierarchical  │  │   • Anki pack     │
│   • Mermaid code  │  │   • JSON          │
└─────────┬─────────┘  └─────────┬─────────┘
          │                      │
          └──────────┬───────────┘
                     ▼
          ┌───────────────────┐
          │     Complete!     │
          │  Open Workspace   │
          └───────────────────┘
```

### AI Interaction Design Principles

**1. Show Progress, Not Mystique**
- Never show a generic spinner for AI tasks
- Show exactly what stage the AI is at
- Show intermediate results when available

**2. Cite Sources**
- Every AI claim cites the source page/paragraph
- Chat responses include `[Source: p.42]` links
- Hovering shows the original text snippet

**3. Allow Interruption**
- User can cancel AI processing at any stage
- Partial results are saved (e.g., notes without flashcards)
- Background processing continues after closing the document

**4. Degrade Gracefully**
- If LLM unavailable → show extracted text + embeddings search only
- If OCR fails → suggest manual text input
- If RAM low → process in smaller chunks

**5. Learning from Interaction**
- AI remembers which flashcard difficulty user prefers
- Adapts quiz question style based on past answers
- Tracks which note formats user edits most

### Chat Context Management

The chat panel always knows which document is active:

```
┌────────────────────────────────────────┐
│ 💬 AI Chat       Context: Quantum Mech  │
├────────────────────────────────────────┤
│                                        │
│ The AI has access to:                  │
│  ✓ Full document text                  │
│  ✓ Generated notes                     │
│  ✓ Flashcards                          │
│  ✓ Quiz questions                      │
│  ✓ Vector embeddings                   │
│                                        │
│ User can also:                         │
│  @reference specific chapter/section   │
│  @flashcard "term" for details          │
│  @mindmap expand on node               │
│  /summarize  (preset commands)         │
│  /quiz       (generate more)          │
│  /flashcard  (generate more)          │
│                                        │
└────────────────────────────────────────┘
```

### Preset AI Commands

| Command | Action |
|---------|--------|
| `/summarize` | Generate new summary at different detail level |
| `/quiz [n]` | Generate n more quiz questions |
| `/flashcard [n]` | Generate n more flashcards |
| `/explain` | Explain current concept in simpler terms |
| `/examples` | Generate more examples |
| `/analogy` | Create an analogy for the concept |
| `/mindmap` | Regenerate or expand mind map |
| `/questions` | Generate important exam questions |
| `/timeline` | Create chronological timeline |

### Streaming Response UI

AI responses stream token-by-token with:
- Typewriter effect (smooth, 30ms per token)
- Markdown rendering in real-time (headings, lists, code appear as tokens arrive)
- Code blocks and tables rendered once complete (to avoid layout shift)
- Streaming indicator while generating: subtle cursor blink
