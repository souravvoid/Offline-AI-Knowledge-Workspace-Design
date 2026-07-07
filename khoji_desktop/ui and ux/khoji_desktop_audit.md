# Khoji Desktop UX & UI Audit

## 1. Existing Design Weaknesses (Mobile Baseline)
- **Navigation:** Bottom bar is too simplified for a power-user desktop app.
- **Hierarchy:** Single-column layout on mobile hides the relationship between raw data (Schema) and processing (Pipeline).
- **Density:** Mobile spacing is too generous for complex knowledge work; desktop needs higher information density.
- **AI Integration:** AI is treated as a viewer (`SCREEN_5`) rather than a persistent collaborator.

## 2. Proposed Design Strategy
- **VS Code Architecture:** Implement a primary sidebar for navigation, a secondary sidebar for AI/Metadata, and a central workspace with tabs.
- **Command-First:** Center the experience around a Command Palette (Cmd+K) for navigation and model control.
- **Persistent Pipeline:** Move the processing status to a status bar and a dedicated panel rather than a full-screen view.

## 3. New Information Architecture
- **Explorer:** Files, Folders, Knowledge Graph.
- **Workspace:** Markdown Editor, PDF Viewer, Schema Inspector, Pipeline Map.
- **Intelligence:** AI Chat, Memory Explorer, Model Manager.
- **Status:** Indexing progress, RAM usage, Model state.

## 4. Prioritized Improvements
1. **Layout (High):** Implement a 3-pane resizable desktop shell.
2. **Typography (Medium):** Shift to a multi-font system (Sans/Serif/Mono).
3. **Workflow (High):** Add keyboard shortcuts for all major views.
4. **AI (Medium):** Streamline memory visualization as a side-panel rather than a main view.
