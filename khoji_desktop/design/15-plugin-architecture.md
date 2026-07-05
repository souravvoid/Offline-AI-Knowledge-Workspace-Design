# Plugin Architecture & SDK

## Vision

Khoji's plugin system allows the community to extend every part of the knowledge pipeline. Think VS Code's extension model, but for a knowledge workspace.

## Plugin Types

```
┌──────────────────────────────────────────────────────────────┐
│                     PLUGIN ECOSYSTEM                          │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │  Parser  │ │   OCR    │ │   LLM    │ │   Exporter   │    │
│  │ Plugins  │ │ Plugins  │ │ Plugins  │ │   Plugins    │    │
│  ├──────────┤ ├──────────┤ ├──────────┤ ├──────────────┤    │
│  │  • DJVU  │ │ • Azure  │ │ • Ollama │ │ • Markdown   │    │
│  │  • XPS   │ │ • Google │ │ • OpenAI │ │ • Anki       │    │
│  │  • CBZ   │ │   Cloud  │ │  (local) │ │ • Notion     │    │
│  │  • HTML  │ │ • Custom │ │ • Custom │ │ • Readwise   │    │
│  │  • Email │ │   Tesser │ │   GGUF   │ │ • Hugo       │    │
│  │  • Chat  │ │   act    │ │ • Claude │ │ • Quartz     │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
│                                                              │
│  ┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │   Diagram    │ │ Citation │ │Translator│ │  Theme   │    │
│  │   Plugins    │ │ Plugins  │ │ Plugins  │ │  Plugins │    │
│  ├──────────────┤ ├──────────┤ ├──────────┤ ├──────────┤   │
│  │ • Graphviz   │ │ • BibTeX │ │ • Libret │ │ • Custom │    │
│  │ • PlantUML   │ │ • Zotero │ │  rans    │ │   CSS    │    │
│  │ • D2         │ │ • Citavi │ │ • Argos  │ │ • Obsidi │    │
│  │ • Excalidraw │ │ • Paperp │ │  Trans   │ │   an     │    │
│  │ • TikZ       │ │   ila    │ │ • Berglas│ │ • Notes  │    │
│  └──────────────┘ └──────────┘ └──────────┘ │   theme  │    │
│                                              └──────────┘    │
│  ┌──────────────┐ ┌──────────┐                                │
│  │    MCP       │ │   Sync   │                                │
│  │   Provider   │ │  Plugin  │                                │
│  ├──────────────┤ ├──────────┤                                │
│  │ • Filesystem │ │ • Git    │                                │
│  │ • GitHub     │ │ • Syncth │                                │
│  │ • Database   │ │   ing    │                                │
│  │ • Web Search │ │ • Nextcl │                                │
│  │ • Terminal   │ │   oud    │                                │
│  └──────────────┘ └──────────┘                                │
└──────────────────────────────────────────────────────────────┘
```

## Plugin API Design

### Architecture

```
┌──────────────────────────────────────────┐
│           Khoji Core (Rust)              │
│  ┌────────────────────────────────────┐  │
│  │        Plugin Host Runtime         │  │
│  │  • Sandboxed execution             │  │
│  │  • Resource limits (CPU, RAM)      │  │
│  │  • Permission system               │  │
│  │  • Lifecycle management            │  │
│  └──────────────┬─────────────────────┘  │
└─────────────────┼────────────────────────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
┌────▼────┐ ┌────▼────┐ ┌────▼────┐
│  WASM   │ │  Native │ │  HTTP   │
│  Plugin │ │  Plugin │ │  Plugin │
│ (Safe)  │ │ (Rust)  │ │ (Any)   │
└─────────┘ └─────────┘ └─────────┘
```

### Plugin Manifest

Every plugin includes a `khoji-plugin.json` manifest:

```json
{
  "id": "khoji-exporter-markdown",
  "name": "Markdown Exporter",
  "version": "1.0.0",
  "description": "Exports knowledge as Markdown files",
  "author": "Khoji Team",
  "license": "MIT",
  "type": "exporter",
  "entry": "main.wasm",
  "permissions": [
    "filesystem:read",
    "filesystem:write",
    "document:read"
  ],
  "hooks": ["on_export", "on_document_processed"],
  "config_schema": {
    "type": "object",
    "properties": {
      "include_frontmatter": {"type": "boolean", "default": true},
      "include_diagrams": {"type": "boolean", "default": true}
    }
  },
  "min_khoji_version": "1.0.0",
  "repository": "https://github.com/khoji/export-markdown"
}
```

### Plugin Lifecycle

```
Installed → Disabled → Enabled → Loaded → Active → Unloaded → Disabled
                ↓                                      ↑
            Removed (uninstalled)                       │
                └──────────────────────────────────────┘
```

### Hook System

Plugins can hook into various pipeline stages:

```rust
// Rust plugin trait example
#[plugin_interface]
trait KhojiPlugin {
    /// Called when plugin is loaded
    fn on_load(&mut self, ctx: &PluginContext) -> Result<()>;
    
    /// Called when plugin is unloaded
    fn on_unload(&mut self) -> Result<()>;
    
    /// Hook: Document processing pipeline
    fn on_document_uploaded(&self, doc: &Document) -> Result<Option<DocumentModification>>;
    fn on_ocr_complete(&self, text: &str, layout: &Layout) -> Result<Option<String>>;
    fn on_extraction_complete(&self, concepts: &[Concept]) -> Result<Option<Vec<Concept>>>;
    fn on_notes_generated(&self, notes: &str) -> Result<Option<String>>;
    
    /// Hook: Export
    fn on_export(&self, doc: &Document, format: &str) -> Result<Option<Vec<u8>>>;
    
    /// Hook: UI
    fn on_sidebar_render(&self) -> Result<Option<HtmlFragment>>;
    fn on_workspace_tab_render(&self, doc: &Document) -> Result<Option<HtmlFragment>>;
    
    /// Hook: Chat
    fn on_chat_message(&self, message: &str, context: &ChatContext) -> Result<Option<String>>;
    
    /// Hook: Custom actions
    fn register_commands(&self) -> Result<Vec<Command>>;
    fn register_keyboard_shortcuts(&self) -> Result<Vec<Shortcut>>;
}
```

### SDK Languages

| Language | Support | Performance | Sandbox |
|----------|---------|-------------|---------|
| **Rust** | First-class | Native | WASM or native |
| **WASM** | First-class | Near-native | Sandboxed |
| **Python** | Via WASM | Moderate | Sandboxed |
| **JavaScript** | Via WASM runtime | Moderate | Sandboxed |
| **Lua** | Embedded | Fast | Sandboxed |
| **Shell** | Via MCP | Slow | Process-level |

### Plugin Store UI

```
┌──────────────────────────────────────────────────────────────┐
│  🧩 Plugin Store                                    [Manage] │
├──────────────────────────────────────────────────────────────┤
│  Search plugins...                                           │
│                                                              │
│  Categories: All │ Exporters │ OCR │ Diagrams │ Themes │ SDK │
│                                                              │
│  ┌─── Markdown Exporter ─────────────────────── [Install] ─┐ │
│  │ Export your knowledge as clean Markdown files with      │ │
│  │ customizable frontmatter and templates.                 │ │
│  │ ⭐ 4.8  ·  12k installs  ·  v1.2.0                      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─── Anki Exporter ──────────────────────────── [Install] ─┐ │
│  │ Export flashcards directly to Anki .apkg format.         │ │
│  │ ⭐ 4.7  ·  8k installs  ·  v1.1.0                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─── Obsidian Sync ─────────────────────────── [Install] ──┐ │
│  │ Sync your Khoji knowledge base directly to Obsidian      │ │
│  │ vault. Bidirectional sync supported.                     │ │
│  │ ⭐ 4.9  ·  5k installs  ·  v0.9.0                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─── BibTeX Citation Manager ───────────────── [Install] ──┐ │
│  │ Auto-extract citations from PDFs and manage BibTeX       │ │
│  │ references.                                              │ │
│  │ ⭐ 4.6  ·  3k installs  ·  v1.0.0                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  [My Plugins] [Discover] [Updates (3)] [SDK Documentation]   │
└──────────────────────────────────────────────────────────────┘
```

### MCP (Model Context Protocol) Support

Khoji supports MCP providers as plugins, enabling AI models to interact with external tools:

```json
{
  "id": "khoji-mcp-github",
  "type": "mcp-provider",
  "tools": [
    {
      "name": "search_repos",
      "description": "Search GitHub repositories",
      "input_schema": {
        "type": "object",
        "properties": {
          "query": {"type": "string"},
          "limit": {"type": "number", "default": 5}
        }
      }
    },
    {
      "name": "get_readme",
      "description": "Get README of a repository",
      "input_schema": {
        "type": "object",
        "properties": {
          "owner": {"type": "string"},
          "repo": {"type": "string"}
        }
      }
    }
  ]
}
```

### Permissions System

Each plugin declares required permissions, and the user approves them:

```
┌──────────────────────────────────────────────────────────────┐
│  🔒 Plugin Permissions                                      │
│                                                              │
│  "BibTeX Citation Manager" requests:                         │
│  ☑ Read document metadata                                   │
│  ☑ Read document full text                                  │
│  ☑ Write to export directory                                │
│  ☐ Access network                                           │
│  ☐ Access clipboard                                         │
│  ☐ Execute shell commands                                   │
│                                                              │
│  [Deny]  [Allow Once]  [Always Allow]                        │
└──────────────────────────────────────────────────────────────┘
```

## Built-in Plugin Examples

### Exporters
- **Markdown Exporter** — Standard `.md` with YAML frontmatter
- **Anki Exporter** — `.apkg` package for Anki desktop/mobile
- **PDF Exporter** — Formatted PDF with diagrams
- **LaTeX Exporter** — `.tex` with proper document structure
- **JSON Exporter** — Structured data for programmatic access
- **Obsidian Vault Exporter** — Direct export to Obsidian vault structure
- **Notion Exporter** — Markdown compatible with Notion import

### OCR Plugins
- **Tesseract OCR** — Default, fast, supports 100+ languages
- **EasyOCR** — Better accuracy, slower, supports 80+ languages
- **Surya OCR** — Best accuracy, GPU recommended

### LLM Plugins
- **Llama.cpp** — Local GGUF models
- **Ollama** — Local models via Ollama API
- **ONNX Runtime** — Quantized models

### Diagram Plugins
- **Mermaid** — Built-in, default
- **Graphviz** — DOT language diagrams
- **PlantUML** — UML diagrams
- **D2** — Modern diagram language
- **Excalidraw** — Hand-drawn style diagrams
- **TikZ** — LaTeX native diagrams
