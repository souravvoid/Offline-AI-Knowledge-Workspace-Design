# Khoji Information Architecture & UX Strategy

## 1. Information Architecture (IA)
### Level 0: The Shell
- **Activity Bar (Far Left):** Global navigation (Explorer, Search, Graph, Memory, Settings).
- **Status Bar (Bottom):** Hardware telemetry (CPU/RAM), model status, indexing progress, versioning.
- **Top Bar:** Breadcrumbs, Workspace title, Sync status, Window controls.

### Level 1: Core Views
- **Onboarding/Home:** Splash → Welcome (File Drop).
- **Processing:** Real-time pipeline visualization (OCR -> Embedding -> AI Synthesis).
- **Workspace (The "Trifecta" Layout):**
    - Left: Library/Navigation.
    - Center: Multi-tab content (Markdown, PDF, Quiz, Mind Map).
    - Right: AI Intelligence Panel (Chat, Definitions, Context).

## 2. Component Library (Khoji Technical Noir)
- **Cards:** Glassmorphic surfaces with `--surface-container-low` background, 1px `--outline-variant` borders.
- **Buttons:**
    - Primary: Solid Indigo (`--primary`), white text.
    - Ghost: Border-only, high-contrast hover state.
- **Typography:**
    - UI: Inter (Variable).
    - Data/Code: JetBrains Mono.
    - Reading: Source Serif Pro (for generated notes).

## 3. User Flow: The Learning Journey
1. **Launch:** Splash screen with animated SVG logo & hardware check.
2. **Action:** Home screen with 4 primary ingestion cards.
3. **Wait:** Processing pipeline shows "Truthful Telemetry" of local AI work.
4. **Learn:** Workspace opens with generated summary & interactive AI sidekick.

## 4. PySide6 Implementation Recommendations
- **Styling:** Use `qt_material` or custom QSS targeting the defined tokens.
- **Performance:** Run all AI/Embedding tasks on `QThread` or `QProcess` to keep the UI thread responsive.
- **Graphics:** Use `QGraphicsView` for the Mind Map and Knowledge Graph.
- **Markdown:** `QTextBrowser` with CSS or `QWebEngineView` for high-fidelity rendering.
