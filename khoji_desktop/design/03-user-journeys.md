# Phase 3: User Journeys

## Journey 1: First-Time User — Document Processing

### Stage 1: Discovery & Installation
| Step | User Action | System Response | Emotion |
|------|------------|-----------------|---------|
| 1 | User downloads Khoji from GitHub Releases | Shows download progress | Anticipation |
| 2 | User installs (one-click installer) | Extracts, checks dependencies | Neutral |
| 3 | First launch | Shows welcome screen with quick start guide | Curious |
| 4 | User sees empty library | Beautiful empty state "Drop your first document" | Intrigued |

### Stage 2: First Document Upload
| Step | User Action | System Response | Emotion |
|------|------------|-----------------|---------|
| 5 | Drags a PDF onto the upload zone | Hover animation, blue glow, "Drop to upload" | Satisfied |
| 6 | Drops the PDF | File accepted animation, shows file name + size | Relieved |
| 7 | Clicks "Process" | Processing modal appears with pipeline visualization | Engaged |
| 8 | Watches AI pipeline | Animated pipeline stages light up sequentially: OCR → Layout → Markdown → Embeddings → LLM → Notes | Fascinated |
| 9 | Processing completes | Success sound, notification, document appears in library | Delighted |

### Stage 3: Exploring Results
| Step | User Action | System Response | Emotion |
|------|------------|-----------------|---------|
| 10 | Opens the processed document | Document workspace opens with tab bar | Curious |
| 11 | Views "Notes" tab | Well-structured Markdown with headings, bullets, bold key terms | Impressed |
| 12 | Clicks "Flashcards" tab | 20+ flashcards auto-generated, cloze deletions and Q&A | Amazed |
| 13 | Clicks "Quiz" tab | 10-question MCQ quiz with difficulty filter | Engaged |
| 14 | Clicks "Mind Map" tab | Interactive Mermaid mind map with zoom/pan | Delighted |
| 15 | Clicks "Timeline" tab | Chronological view of events/concepts from the document | Surprised |

### Stage 4: AI Chat
| Step | User Action | System Response | Emotion |
|------|------------|-----------------|---------|
| 16 | Opens chat panel (right sidebar) | Chat panel slides in with context indicator | Curious |
| 17 | Types "Explain the main theorem" | AI responds with context from the document, cites page numbers | Satisfied |
| 18 | Types "Create more examples" | AI generates additional examples in Markdown | Impressed |
| 19 | Follows up with "Make it simpler" | AI re-explains with simpler language, analogies | Grateful |

### Stage 5: Export
| Step | User Action | System Response | Emotion |
|------|------------|-----------------|---------|
| 20 | Clicks Export button | Export dialog with formats: Markdown, Anki, PDF, LaTeX, JSON | Curious |
| 21 | Selects Markdown export | Opens file save dialog | Neutral |
| 22 | Saves to local folder | .md files saved with frontmatter, images extracted | Satisfied |
| 23 | Opens in Obsidian/VS Code | Clean Markdown renders perfectly | Delighted |

---

## Journey 2: Returning User — Semantic Search

| Step | User Action | System Response | Emotion |
|------|------------|-----------------|---------|
| 1 | Opens Khoji (startup <3s) | Library loads with cached thumbnails | Satisfied |
| 2 | Cmd+K (global search) | Search modal opens with keyboard focus | Fast |
| 3 | Types "neural networks backpropagation" | Results appear instantly (local vector search), ranked by relevance | Impressed |
| 4 | Searches across 50 documents | Results show document title, page number, snippet with keyword highlight | Satisfied |
| 5 | Clicks a result | Opens document at exact location | Precise |
| 6 | Asks chat "Explain this part more" | Chat opens with document context pre-loaded | Seamless |

---

## Journey 3: Daily Study Session — Spaced Repetition

| Step | User Action | System Response | Emotion |
|------|------------|-----------------|---------|
| 1 | Opens Khoji | Shows dashboard: "3 documents due for review" | Organized |
| 2 | Clicks "Review" | Opens flashcard review mode, full-screen, minimal UI | Focused |
| 3 | Sees a flashcard | Card shows question, thinks about answer | Thinking |
| 4 | Clicks "Show Answer" | Card flips with animation, shows answer with source reference | Learning |
| 5 | Rates "Easy" | Card scheduled for next review in 3 days | Progress |
| 6 | Rates "Hard" | Card rescheduled for today/tomorrow | Adaptive |
| 7 | Completes review queue | Shows stats: 20 cards reviewed, 85% retention | Motivated |

---

## Journey 4: Professor Preparing Course Material

| Step | User Action | System Response | Emotion |
|------|------------|-----------------|---------|
| 1 | Opens Khoji | Library with 30+ documents | Familiar |
| 2 | Creates new collection "ECON 201 - Macroeconomics" | Collection created, empty state | Organized |
| 3 | Drags 3 textbook PDFs into collection | Files queued for batch processing | Productive |
| 4 | Clicks "Process All" | Pipeline runs sequentially, shows progress per document | Patient |
| 5 | After processing, opens "Quiz" tab | Finds 30 questions generated | Impressed |
| 6 | Edits quiz: deletes 5, adds 2 custom questions | Inline editing, saves automatically | In Control |
| 7 | Exports quiz to Moodle XML format | Download ready | Efficient |
| 8 | Shares collection link (local network export) | Students on LAN can import (future feature) | Collaborative |

---

## Journey 5: Error Recovery — OCR Failure

| Step | User Action | System Response | Emotion |
|------|------------|-----------------|---------|
| 1 | Uploads a scanned image PDF | Processing starts normally | Hopeful |
| 2 | OCR stage fails (poor quality scan) | Pipeline pauses, shows error state with clear message | Frustrated |
| 3 | Error state shows: "OCR could not read this document. Try: (1) Higher quality scan (2) Different language model (3) Manual text entry" | Actionable suggestions | Guided |
| 4 | User clicks "Try different OCR model" | Model selection dropdown | Curious |
| 5 | Selects "Tesseract v5 + English" | Re-processes with alternate model | Hopeful |
| 6 | Processing succeeds | User is relieved; error state was helpful, not blocking | Relieved |

---

## Journey 6: Complete Learning Loop (Extended)

```
Week 1:
  Upload → Process → Review Notes → Browse Flashcards → Take Quiz
Week 2:
  Open Khoji → Review due flashcards → Chat to clarify doubts → Update notes
Week 4:
  Search across documents → Find related concepts → Create collection
  → Export comprehensive study guide → Share with study group
Week 8:
  Open Khoji → Re-upload updated edition → Diff against previous notes
  → Only new/changed content processed → Insights on what changed
```
