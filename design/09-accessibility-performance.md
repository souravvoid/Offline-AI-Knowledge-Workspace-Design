# Phase 13-14: Accessibility & Performance

## Accessibility Checklist (WCAG 2.1 AA)

### Perceivable

| Check | Status | Implementation |
|-------|--------|----------------|
| Text alternatives for non-text content | P0 | All icons have aria-labels; images have alt text |
| Captions for audio/video | P2 | N/A (no media content) |
| Info and relationships preserved in structure | P0 | Semantic HTML: `<nav>`, `<main>`, `<article>`, `<aside>` |
| Meaningful sequence | P0 | Logical DOM order matches visual order |
| Sensory characteristics not sole means | P0 | Don't rely on color/shape alone; use text labels |
| Color contrast (4.5:1 text, 3:1 large) | P0 | All color pairs validated against contrast ratios |
| Resize text up to 200% without loss | P0 | Use relative units (rem), no text truncation at zoom |
| Images of text | P0 | Never use images for text content |
| Reflow to 320px width without scroll | P1 | Responsive grid; horizontal scroll only for data tables |

### Operable

| Check | Status | Implementation |
|-------|--------|----------------|
| All functionality via keyboard | P0 | Tab indices, focus management, no keyboard traps |
| No keyboard traps | P0 | Escape closes modals/menus; Tab cycles through controls |
| Focus order preserves meaning | P0 | Logical tab order matching visual layout |
| Link purpose from text alone | P0 | Descriptive link text (no "click here") |
| Multiple ways to find content | P0 | Library + Search + Collections + Recent |
| Skip to content link | P0 | First focusable element on page |
| Focus visible (2px ring) | P0 | Custom focus-visible styles, never `outline: none` |
| Language of page | P0 | `lang` attribute set dynamically |
| No flashing content >3Hz | P0 | No strobe effects; animations are subtle |
| Pointer gestures not required | P1 | All touch gestures have button alternatives |
| Motion actuation not required | P1 | Shake/device motion not used |
| Pointer cancel | P0 | No down-event triggers; use click/up events |
| Label in name | P0 | Accessible names match visible labels |
| Status messages announced | P0 | aria-live regions for processing, errors, notifications |

### Understandable

| Check | Status | Implementation |
|-------|--------|----------------|
| Language of page | P0 | `lang` attribute on `<html>` |
| Language of parts | P2 | For mixed-language documents |
| On focus does not cause context change | P0 | No auto-submit on focus |
| On input does not cause context change | P0 | No auto-actions on input events |
| Consistent navigation | P0 | Sidebar and top bar consistent across all views |
| Consistent identification | P0 | Same icons/labels for same functions everywhere |
| Error identification | P0 | Clear error messages with suggestions |
| Labels or instructions | P0 | All form fields have labels, inputs have placeholders |
| Suggestions for errors | P0 | "Did you mean...?" for search, "Try higher quality scan" for OCR |
| Error prevention (legal/financial) | P2 | N/A |
| Help and documentation | P1 | Tooltips, quick-start guide, keyboard shortcut cheat sheet |

### Robust

| Check | Status | Implementation |
|-------|--------|----------------|
| Parsing (no duplicate IDs) | P0 | Linting ensures valid HTML |
| Name, Role, Value | P0 | All custom components have ARIA roles and properties |
| Status messages | P0 | aria-live="polite" for dynamic updates |

### Keyboard Shortcuts Reference

```
Global           ─────────────────────────────────
⌘K              Search all documents and notes
⌘N              New note
⌘,              Open settings
⌘⇧U             Upload document
⌘W              Close current tab/panel

Navigation       ─────────────────────────────────
⌘1              Library
⌘2              Notes
⌘3              Flashcards
⌘4              Quiz
⌘5              Mind Maps
⌘6              Chat history
⌘B              Toggle sidebar
⌘⇧L             Toggle right panel (chat)
⌘⇧D             Toggle dark mode

Document         ─────────────────────────────────
⌘Enter          Send AI chat message
⌘P              Toggle preview/edit mode
⌘E              Export document
⌘F              Find in document
⌘S              Save (auto-saves, but manual trigger)
⌘Z              Undo
⌘⇧Z             Redo

Flashcard Review ─────────────────────────────────
Space           Show/hide answer
1               Again (1 min)
2               Hard (5 min)
3               Good (1 day)
4               Easy (3 days)
→               Next card
←               Previous card
R               Restart queue

Quiz             ─────────────────────────────────
A/B/C/D         Select answer option
Enter           Confirm/submit answer
→               Next question
←               Previous question
Tab             Focus next element

Accessibility    ─────────────────────────────────
⌘⇧A             Toggle high contrast mode
⌘+              Increase font size
⌘-              Decrease font size
⌘0              Reset font size
```

---

## Performance Strategy

### Target Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Startup time | <3s cold, <1s warm | `performance.now()` |
| Document list render | <100ms (100 items) | React profiler |
| Search results | <50ms (local vector search) | `performance.mark()` |
| Flashcard flip | <16ms (60fps) | DevTools FPS |
| Quiz render | <100ms | React profiler |
| Export (Markdown) | <500ms for 100pg doc | Timer |
| Export (Anki) | <2s for 100 cards | Timer |
| AI Chat response | <100ms first token | Timer |
| Memory usage | <500MB idle, <1.5GB processing | `performance.memory` |
| Disk usage | <2GB (base) + model storage | File system API |
| CPU usage | <10% idle, <80% processing | OS task manager |

### Architecture for Performance

```
┌─────────────────────────────────────────────────────────┐
│                    UI Layer (Tauri/Electron)              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ React/Vue   │  │ Markdown    │  │ Mermaid Render   │  │
│  │ (Virtual)   │  │ Renderer    │  │ (SVG via mm)     │  │
│  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘  │
│         │                │                   │           │
│  ┌──────┴────────────────┴───────────────────┴────────┐  │
│  │              IPC Bridge (Commands)                   │  │
│  └──────────────────────┬──────────────────────────────┘  │
├─────────────────────────┼────────────────────────────────┤
│                Rust/Python Backend                        │
│  ┌──────────────────────┴──────────────────────────────┐  │
│  │                   Orchestrator                       │  │
│  ├────────┬────────┬────────┬────────┬────────────────┤  │
│  │  OCR   │  Text  │ Embed  │  LLM   │  Vector DB     │  │
│  │ Module │Extract │Module  │ Module │  (SQLite+vec)   │  │
│  ├────────┴────────┴────────┴────────┴────────────────┤  │
│  │               Worker Pool (CPU threads)              │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Performance Optimization Techniques

#### 1. Lazy Loading

| Component | Strategy |
|-----------|----------|
| Sidebar items | Load on sidebar mount |
| Document list | Virtual scroll (render 20+ buffer) |
| Tab content | Load tab content on tab selection |
| Mind map | Lazy render SVG, progressive reveal |
| AI Chat history | Load last 20, paginate older |
| Export preview | Generate on demand, cache result |
| Empty states | Always eager (tiny bundle) |
| Error states | Always eager (tiny bundle) |

#### 2. Virtual Scrolling

Use virtual scrolling for:
- Document library (if >50 items)
- Flashcard review queue
- Chat message history
- Search results
- Note list

Virtual scroll window: 3x viewport height (1x buffer above, 1x buffer below)

#### 3. Caching Strategy

| Cache | Type | Size | Eviction |
|-------|------|------|----------|
| Document thumbnails | LRU | 50 items | Least recently used |
| Vector search index | Persistent | Per document | Manual rebuild |
| AI chat sessions | Persistent | Last 20 | Oldest first |
| Rendered Mermaid SVGs | LRU | 20 diagrams | Least recently used |
| Recent search results | TTL | 10 items | 5 minutes |
| Model metadata | Persistent | Small | Manual refresh |
| User preferences | Persistent | Small | N/A |

#### 4. Background Processing

- Document processing runs in a Web Worker / Rust thread
- UI remains responsive during processing
- User can navigate away and return to completed document
- Queue multiple documents for sequential processing
- Process during idle time (RequestIdleCallback)

#### 5. Incremental Processing

```
Phase 1 (Immediate):   OCR + Text Extraction → Show raw text
Phase 2 (Fast):        Embeddings → Enable search
Phase 3 (Medium):      LLM Summary + Notes
Phase 4 (Slow):        Flashcards + Quiz + Mind Map

User sees immediate value while full processing completes.
```

#### 6. Memory Management

| Strategy | Implementation |
|----------|----------------|
| Document unloading | Unload document text from memory when switching away |
| Model unloading | Unload LLM from GPU/memory when idle for 5min |
| Image downsizing | Downscale document page images to 200dpi for display |
| WebGL fallback | Use CPU path for models when GPU memory low |
| Chunked processing | Process large documents in 10-page chunks |
| Garbage collection hint | `performance.mark('gc-start')` after heavy operations |

#### 7. Disk & Storage

| Item | Estimated Size |
|------|---------------|
| Application | 50MB |
| Base models (OCR + Embeddings) | 200MB |
| Small LLM (1B parameters) | 600MB |
| Medium LLM (3B parameters) | 2GB |
| Vector database (per 100 docs) | 100MB |
| Document storage (per 100 PDFs) | 500MB |
| Cache | 200MB |

Total base: ~1GB with small LLM
Total with medium LLM: ~2.5GB

### Low RAM Mode (4GB devices)

When system RAM < 6GB:
1. Use smallest available LLM (0.5B parameters)
2. Process documents in smaller chunks (5 pages)
3. Reduce embedding dimensions (384→128)
4. Unload models immediately after processing
5. Disable mind map auto-generation (manual trigger only)
6. Limit concurrent workers to 2
7. Show RAM usage warning at 80% utilization
8. Suggest closing other applications
9. Use SQLite instead of in-memory vector store

### Low GPU / CPU-only Mode

When no GPU detected:
1. Use ONNX runtime with CPU execution provider
2. Reduce batch sizes for embedding generation
3. Use quantized models (INT8, not FP16)
4. Process documents sequentially, not in parallel
5. Show estimated processing time (slower but works)
6. Use lighter OCR model (Tesseract instead of EasyOCR)
7. Disable real-time preview during processing
