# Phase 4: Information Architecture

## Global Navigation Structure

```
Khoji Workspace
│
├── 📚 Library                    [Primary - P0]
│   ├── Documents (grid/list view)
│   ├── Collections (tag groups)
│   ├── Recent (last 10)
│   └── Favorites (starred)
│
├── 📝 Notes                      [Primary - P0]
│   ├── All Notes
│   ├── By Document
│   ├── By Collection
│   └── Search Notes
│
├── 🃏 Flashcards                 [Primary - P0]
│   ├── All Cards
│   ├── Review Queue (spaced repetition)
│   ├── By Document
│   ├── By Difficulty
│   └── Statistics
│
├── ❓ Quiz                       [Primary - P0]
│   ├── Generate Quiz
│   ├── Take Quiz (fullscreen)
│   ├── Results
│   └── History
│
├── 🧠 Mind Maps                  [Secondary - P1]
│   ├── All Maps
│   ├── Interactive Viewer
│   └── Export
│
├── 💬 AI Chat                    [Primary - P0]
│   ├── Chat Sessions
│   ├── Context (active document)
│   ├── History
│   └── System Prompts
│
├── 🔍 Semantic Search            [Primary - P0]
│   ├── Search All
│   ├── Search in Document
│   ├── Search Filters
│   └── Search History
│
├── 📊 Dashboard                  [Secondary - P1]
│   ├── Recent Activity
│   ├── Review Due
│   ├── Stats (documents, cards, notes)
│   └── Quick Actions
│
├── ⚙️ Settings                   [Secondary - P1]
│   ├── General
│   │   ├── Theme (light/dark/system)
│   │   ├── Language
│   │   └── Startup Behavior
│   ├── Models
│   │   ├── Download Manager
│   │   ├── Model Selection (OCR, Embeddings, LLM)
│   │   └── Storage Usage
│   ├── Storage
│   │   ├── Data Location
│   │   ├── Auto-Export
│   │   └── Cache Management
│   ├── Export
│   │   ├── Default Format
│   │   ├── Templates
│   │   └── Auto-Export Rules
│   ├── Keyboard Shortcuts
│   └── Accessibility
│       ├── Font Size
│       ├── High Contrast
│       └── Screen Reader
│
└── 🗂️ Collections                [Secondary - P1]
    ├── Create Collection
    ├── Smart Collections (auto-rules)
    └── Shared Collections (LAN)
```

## Workspace Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Top Bar: Logo | Tab Bar | Search (Cmd+K) | User Menu       │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                  │
│ Sidebar  │              Main Content Area                   │
│ (Collaps)│                                                  │
│          │   ┌─────────────────────────────────────────┐    │
│ Library  │   │  Tab: Notes │ Flashcards │ Quiz │ ...   │    │
│ Notes    │   ├─────────────────────────────────────────┤    │
│ Cards    │   │                                         │    │
│ Quiz     │   │         Content View                    │    │
│ Chat     │   │                                         │    │
│ Search   │   │                                         │    │
│ Settings │   │                                         │    │
│          │   └─────────────────────────────────────────┤    │
│          │   │  Status Bar: Model Status │ Progress     │    │
├──────────┴──────────────────────────────────────────────────┤
│  Pipeline Status Bar (processing indicator)                  │
└─────────────────────────────────────────────────────────────┘
```

## Document Workspace (Contextual)

When a document is selected, the workspace transforms:

```
┌────────────────────────────────────────────────────────────┐
│ ← Back to Library  │  "Quantum Mechanics" │ ⭐ ⋮           │
├──────────┬────────────────────────────────┬────────────────┤
│          │                                │                │
│ Outline  │   Tab Content Area             │  AI Chat       │
│ (Doc TOC)│                                │  (Right Panel) │
│          │  ┌────────────────────────┐    │                │
│ ├ Intro  │  │                        │    │  Ask about    │
│ ├ Ch 1   │  │  Tab: Notes            │    │  this doc...  │
│ ├ Ch 2   │  │  Flashcards            │    │                │
│ ├ Ch 3   │  │  Quiz                  │    │  ┌──────────┐ │
│          │  │  Mind Map              │    │  │ Response │ │
│          │  │  Timeline              │    │  │          │ │
│          │  │                        │    │  └──────────┘ │
│          │  └────────────────────────┘    │                │
│          │                                │  [Ask] [Clear] │
├──────────┴────────────────────────────────┴────────────────┤
│  5 notes  │  20 flashcards  │  Quiz ready │  Exported 2x   │
└────────────────────────────────────────────────────────────┘
```

## Navigation Hierarchy

### Level 1: App-Level
- Library (default landing)
- Dashboard (optional landing for returning users)
- Search (overlay, Cmd+K)

### Level 2: Document-Level
- Notes View
- Flashcards View
- Quiz View
- Mind Map View
- Timeline View
- Summary View
- Important Questions

### Level 3: Interaction-Level
- Chat (right sidebar)
- Edit Note
- Take Quiz
- Review Flashcards
- Export Dialog
- Settings Drawer

## Screen Flow

```
                  ┌───────────┐
                  │  Splash   │ (first launch: setup wizard)
                  └─────┬─────┘
                        │
                  ┌─────▼─────┐
                  │  Library  │◄───────┐
                  └─────┬─────┘        │
                        │              │
                  ┌─────▼─────┐        │
                  │  Upload   │        │
                  └─────┬─────┘        │
                        │              │
                  ┌─────▼─────┐        │
                  │Processing │        │
                  └─────┬─────┘        │
                        │              │
              ┌─────────┴──────────┐   │
              │                    │   │
        ┌─────▼──────┐   ┌────────▼──┐│
        │ Workspace  │   │  Settings ││
        └─────┬──────┘   └──────────┘│
              │                      │
     ┌───────┬┴────┬───────┐        │
     │       │     │       │        │
  ┌──▼──┐ ┌──▼──┐ ┌▼───┐ ┌▼───┐    │
  │Notes│ │Flash│ │Quiz│ │Mind│    │
  └──┬──┘ │cards│ │    │ │Map │    │
     │    └──┬──┘ └──┬─┘ └──┬─┘    │
     └───────┴───────┴──────┘      │
                        │          │
                  ┌─────▼─────┐    │
                  │  Export   │    │
                  └───────────┘    │
                        │          │
                        └──────────┘
```
