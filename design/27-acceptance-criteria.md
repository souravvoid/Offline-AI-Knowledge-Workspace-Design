# Acceptance Criteria

Every feature's pass/fail criteria for testing and validation.

---

## Feature: Document Upload

```
P0 — Must work for MVP

✓ Drag and drop single file onto upload zone
✓ Click upload zone to open file picker
✓ Upload PDF, PNG, JPG, WEBP, PPT, PPTX, DOC, DOCX, EPUB
✓ Show file name and size after selection
✓ Show file type icon matching the format
✓ Cancel upload before processing starts
✓ Show error for unsupported file types
✓ Show error for files >200MB
✓ Show error for corrupted files
✓ Show error for password-protected PDFs
✓ Queue multiple files for batch upload
✓ Drag over highlight animation
✓ File accepted confirmation animation
✓ Keyboard accessible (Tab + Enter to upload)
✓ Screen reader announces upload progress
✓ Works offline with no network
✓ Handle files with unicode names
✓ Handle files with spaces in names
```

## Feature: Document Processing

```
P0 — Must work for MVP

✓ Processing starts after upload
✓ Show pipeline visualization with 8 stages
✓ Show current stage name and status
✓ Show overall progress percentage
✓ Show estimated time remaining
✓ Completed stages show green checkmark
✓ Current stage shows pulsing indicator
✓ Failed stage shows red X with error message
✓ Append new documents to processing queue
✓ Cancel processing mid-pipeline
✓ Partial results saved on cancel (notes without flashcards)
✓ Resume cancelled processing
✓ Retry failed processing
✓ Background processing (user can navigate away)
✓ Processing completes with notification
✓ Processing time within 2 minutes for 100-page PDF
✓ Low memory mode activates automatically when <6GB RAM
✓ Screen reader announces pipeline status changes
```

## Feature: Notes View

```
P0 — Must work for MVP

✓ Display AI-generated Markdown notes
✓ Render headings correctly (h1 → h6 hierarchy)
✓ Render bold, italic, strikethrough text
✓ Render ordered and unordered lists
✓ Render code blocks with syntax highlighting
✓ Render blockquotes
✓ Render tables
✓ Render LaTeX formulas ($$...$$ and $...$)
✓ Render Mermaid diagrams
✓ Render horizontal rules
✓ Render links as clickable
✓ Render images from document
✓ Show YAML frontmatter metadata
✓ Toggle between rendered view and source Markdown
✓ Edit notes inline (source mode)
✓ Auto-save edited notes
✓ Notes persist after app restart
✓ Copy notes to clipboard
✓ Find in notes (Ctrl+F)
✓ Outline panel generates from heading structure
✓ Click heading in outline → scroll to position
✓ Reading mode (serif font, wider text)
✓ Screen reader reads Markdown content
```

## Feature: Flashcards

```
P0 — Must work for MVP

✓ Display list of generated flashcards
✓ Filter by difficulty (easy, medium, hard)
✓ Filter by tag
✓ Search flashcards by text
✓ Sort by created date, difficulty, source page
✓ View card count per document
✓ Delete individual cards
✓ Regenerate cards (delete all + regenerate)
✓ Enter full-screen review mode
✓ Show one card at a time in review mode
✓ Tap/click to flip card (3D animation)
✓ Show answer rating after flip
✓ Rate: Again (1 min), Hard (5 min), Good (1 day), Easy (3 days)
✓ Keyboard: Space=flip, 1-4=rate, →=next
✓ Next card appears after rating
✓ Show progress (5 of 20)
✓ Show review session stats at end
✓ Cards scheduled via SM-2 algorithm
✓ Due cards count shown on dashboard
✓ Retention rate tracked per card
✓ Weak topic identification
✓ Session statistics: cards, correct%, time, streak
✓ Export flashcards to Anki .apkg
✓ Anki export preserves tags and difficulty
```

## Feature: Quiz

```
P0 — Must work for MVP

✓ Display list of generated questions
✓ Filter by difficulty (easy, medium, hard)
✓ Filter by topic
✓ Choose number of questions (5, 10, 15, 20, all)
✓ Start quiz session
✓ Show one question at a time
✓ Show MCQ options as buttons (A/B/C/D)
✓ Keyboard: A-D to select, Enter to confirm
✓ Show question progress (3 of 10)
✓ Show timer (configurable)
✓ Submit answer → show correct/incorrect
✓ Show explanation after each answer
✓ Green highlight for correct, red for wrong
✓ Move to next question automatically
✓ Flag question for later review
✓ Skip question (mark as unanswered)
✓ Review all answers at end
✓ Show final score (percentage + correct/total)
✓ Show topic breakdown (which topics were weak)
✓ Show time taken
✓ Review missed questions with correct answers
✓ Restart quiz with same questions
✓ Generate new quiz with different questions
✓ Export quiz to Markdown/PDF
✓ Distractors are plausible (not obviously wrong)
✓ Questions are verifiable from source
```

## Feature: Mind Maps & Diagrams

```
P1 — Should work for MVP

✓ Display generated Mermaid diagrams
✓ Render flowcharts, mind maps, timelines, ER diagrams
✓ Zoom in/out with scroll
✓ Pan by dragging background
✓ Fit diagram to viewport
✓ Reset zoom/pan
✓ Export diagram as SVG
✓ Export diagram as PNG
✓ Copy Mermaid code to clipboard
✓ Show diagram title and description
✓ Show diagram source section reference
✓ Interactive nodes (click for details)
✓ Layout algorithm selection (force/hierarchical/radial)
✓ Dark mode support in diagrams
✓ Responsive to panel resize
✓ Regenerate individual diagram
✓ Multiple diagrams per document
```

## Feature: AI Chat

```
P0 — Must work for MVP

✓ Open chat panel
✓ Show context: current document name
✓ Type message in input
✓ Send message (Enter or Send button)
✓ Receive AI response with streaming tokens
✓ Typewriter animation for streaming
✓ Show citations as [Page: XX] links
✓ Click citation → scroll to source
✓ Conversation history per session
✓ Create new chat session
✓ Switch between chat sessions
✓ Clear chat history
✓ Copy AI response to clipboard
✓ Retry failed response
✓ Cancel generating response
✓ /summarize command
✓ /quiz [n] command
✓ /flashcard [n] command
✓ /explain command
✓ /examples command
✓ /analogy command
✓ /questions command
✓ Follow-up questions maintain context
✓ Slash-command autocomplete on / 
✓ Response adapts to user level (from memory)
✓ Chat persists after app restart
✓ Chat exports with document export
✓ Offline when model unavailable
```

## Feature: Semantic Search

```
P0 — Must work for MVP

✓ Open search with Cmd+K
✓ Focus input automatically
✓ Type query → show results as you type
✓ Debounce input (300ms)
✓ Show results ranked by relevance score
✓ Show result snippets with query highlighted
✓ Show document title for each result
✓ Show page number for each result
✓ Show relevance score as progress bar
✓ Click result → open document at page
✓ Filter by document
✓ Filter by collection
✓ Filter by file type
✓ Filter by date range
✓ Clear search with Escape
✓ Close search modal with Escape
✓ Navigate results with arrow keys
✓ Select result with Enter
✓ Show "no results" state with suggestions
✓ Search across all processed documents
✓ Hybrid search (vector + keyword BM25)
✓ Search history (last 10 queries)
✓ Works fully offline
✓ Results appear in <100ms
```

## Feature: Export

```
P0 — Must work for MVP

✓ Open export dialog
✓ Select export format: Markdown, Anki, PDF, LaTeX, JSON, CSV, TXT
✓ Show format description and file size estimate
✓ Recommended format badge on Markdown
✓ Include/exclude: notes, flashcards, quiz, diagrams, images
✓ Choose output directory
✓ Export with progress indicator
✓ Open export folder when complete
✓ Show success notification
✓ Handle disk full error
✓ Handle permission denied error
✓ Markdown export: valid .md with frontmatter
✓ Anki export: valid .apkg importable in Anki
✓ PDF export: readable formatting
✓ LaTeX export: compilable document
✓ JSON export: parseable structure
✓ CSV export: importable in spreadsheet
```

## Feature: Collections

```
P1 — Should work for MVP

✓ Create new collection
✓ Name collection
✓ Add description
✓ Choose color
✓ Choose icon
✓ Add documents to collection
✓ Remove documents from collection
✓ Delete collection (doesn't delete documents)
✓ List all collections
✓ Show document count per collection
✓ Filter library by collection
✓ Drag document onto collection to add
✓ Reorder collections
✓ Smart collections with auto-rules
✓ Nested collections (parent/child)
```

## Feature: Settings

```
P1 — Should work for MVP

✓ Open settings drawer
✓ Switch theme: Light, Dark, System
✓ Change font size: Small, Medium, Large, X-Large
✓ Toggle reading mode (serif/sans)
✓ Change language
✓ Set default export format
✓ Toggle sidebar visibility
✓ Manage AI models
✓ Download models with progress
✓ Delete downloaded models
✓ View model sizes
✓ Change data storage location
✓ Clear cache
✓ View total storage used
✓ Reset all data (with confirmation)
✓ View app version
✓ Keyboard shortcuts reference
✓ Accessibility settings (high contrast, reduce motion)
✓ All settings persist across restarts
```

## Feature: Dark Mode

```
P0 — Must work for MVP

✓ Toggle between light and dark themes
✓ All UI components render correctly in dark mode
✓ All colors meet WCAG AA contrast in dark mode
✓ Markdown notes render with proper dark colors
✓ Mermaid diagrams render with dark theme
✓ Chat bubbles with proper dark colors
✓ Knowledge graph with proper dark colors
✓ Icons visible in dark mode
✓ Text readable in dark mode
✓ Shadows visible in dark mode
✓ Images from documents visible (no dark overlay)
✓ System theme detection on startup
✓ Smooth transition between themes
```

## Feature: Keyboard Navigation

```
P0 — Must work for MVP

✓ Tab through all interactive elements
✓ Visible focus indicator on all elements
✓ Enter activates focused element
✓ Space activates focused button
✓ Escape closes modals, dropdowns, search
✓ Arrow keys navigate lists
✓ Cmd+K opens search from anywhere
✓ Cmd+1-6 switches sidebar tabs
✓ Cmd+B toggles sidebar
✓ Cmd+D toggles dark mode
✓ Cmd+E opens export
✓ Cmd+, opens settings
✓ Cmd+Shift+U opens upload
✓ Flashcard review: Space, 1-4, →, ←
✓ Quiz: A/B/C/D, Enter, Tab
✓ Tab order is logical (top to bottom, left to right)
✓ No keyboard traps
✓ Skip to content link on all pages
```

## Feature: Accessibility

```
P0 — Must work for MVP

✓ All images have alt text
✓ All icons have aria-labels
✓ All form inputs have labels
✓ Color contrast >4.5:1 for normal text
✓ Color contrast >3:1 for large text
✓ Focus indicators on all interactive elements
✓ Skip to main content link
✓ Semantic HTML (nav, main, article, aside, footer)
✓ ARIA landmarks on all sections
✓ headings in correct order (no skipping levels)
✓ aria-live regions for dynamic content
✓ aria-expanded for expandable elements
✓ aria-current for active navigation
✓ role="status" for notifications
✓ role="alert" for errors
✓ role="dialog" for modals
✓ role="tablist" for tabs
✓ prefers-reduced-motion respected
✓ prefers-color-scheme respected
✓ Screen reader announces page changes
✓ Screen reader announces processing progress
✓ Screen reader announces search results count
✓ Font size can be increased to 200% without loss
```

## Feature: Error Recovery

```
P0 — Must work for MVP

✓ OCR failure → show suggestions (higher DPI, different engine, manual entry)
✓ Model not found → show download prompt with size
✓ Out of memory → show optimization suggestions, low-mem mode
✓ Corrupted file → show error details, suggest re-download
✓ Unsupported format → show list of supported formats
✓ Storage full → show cleanup wizard
✓ AI chat error → retry button, model switch option
✓ Network required for model download → show queue
✓ Processing cancellation → confirm dialog
✓ Document deletion → confirm dialog
✓ Settings reset → confirm dialog
✓ All errors have clear, actionable messages
✓ No generic "Something went wrong" messages
✓ Errors are announced to screen readers
```

## Feature: Performance

```
P0 — Must work for MVP

✓ App starts in <3s (cold start)
✓ App starts in <1s (warm start)
✓ Library renders in <100ms with 100 documents
✓ Search returns results in <50ms
✓ Chat first token in <100ms
✓ Flashcard flip at 60fps
✓ Quiz renders in <100ms
✓ Markdown export in <500ms for 100-page doc
✓ Anki export in <2s for 100 cards
✓ Memory idle <200MB
✓ Memory processing <1.5GB
✓ No visible jank during normal use
✓ Smooth scrolling at 60fps
✓ No memory leaks (tested with 10 upload/delete cycles)
✓ Models unload after 5 minutes idle
✓ Processing in background does not block UI
```

## Feature: Knowledge Graph

```
P2 — Post-MVP

✓ Concepts extracted from document
✓ Relationships detected between concepts
✓ Nodes displayed in force-directed graph
✓ Click node → show detail panel
✓ Drag node to reposition
✓ Hover highlights connected nodes
✓ Zoom with scroll
✓ Pan by dragging background
✓ Fit graph to viewport
✓ Layout algorithm selection
✓ Concept types distinguished visually
✓ Cross-document connections discovered
✓ Backlinks generated in Markdown
✓ Search within graph
✓ Detail panel shows source documents
✓ Detail panel shows connections
✓ Detail panel shows actions (view notes, generate cards)
```
