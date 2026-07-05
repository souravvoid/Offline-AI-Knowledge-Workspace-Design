"""Notes view — markdown editor for document notes with live preview."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from khoji.database.db import Database


class NotesView(QWidget):
    """Notes panel with markdown editor and preview."""

    notes_saved = Signal(str)

    def __init__(self, db: Database, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self._doc_id: str | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        self._title = QLabel("Notes")
        self._title.setObjectName("heading")
        header.addWidget(self._title)
        header.addStretch()

        self._doc_label = QLabel("")
        self._doc_label.setObjectName("muted")
        header.addWidget(self._doc_label)

        save_btn = QPushButton("💾  Save")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self._save_notes)
        header.addWidget(save_btn)
        layout.addLayout(header)

        # Splitter: Editor | Preview
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Editor
        editor_frame = QFrame()
        editor_layout = QVBoxLayout(editor_frame)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_label = QLabel("  Editor")
        editor_label.setObjectName("muted")
        editor_layout.addWidget(editor_label)

        self._editor = QTextEdit()
        self._editor.setPlaceholderText("Write your notes here (Markdown supported)...")
        self._editor.textChanged.connect(self._on_text_changed)
        editor_layout.addWidget(self._editor, 1)
        splitter.addWidget(editor_frame)

        # Preview
        preview_frame = QFrame()
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_label = QLabel("  Preview")
        preview_label.setObjectName("muted")
        preview_layout.addWidget(preview_label)

        self._preview = QTextEdit()
        self._preview.setReadOnly(True)
        self._preview.setObjectName("card")
        preview_layout.addWidget(self._preview, 1)
        splitter.addWidget(preview_frame)

        splitter.setSizes([500, 500])
        layout.addWidget(splitter, 1)

        # Empty state
        self._empty = QLabel("Select a document from the Library to view/edit notes.")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setObjectName("muted")
        layout.addWidget(self._empty)

    def load_document(self, doc_id: str) -> None:
        """Load notes for a document."""
        self._doc_id = doc_id
        doc = self.db.get_document(doc_id)
        if not doc:
            return

        self._title.setText(f"Notes — {doc.get('title', doc['filename'])}")
        self._doc_label.setText(doc["filename"])

        notes = self.db.get_notes(doc_id)
        if notes:
            self._editor.setPlainText(notes.get("content", ""))
        else:
            self._editor.clear()

        self._empty.setVisible(False)
        self._editor.setVisible(True)
        self._preview.setVisible(True)

    def _on_text_changed(self) -> None:
        content = self._editor.toPlainText()
        html = self._markdown_to_html(content)
        self._preview.setHtml(html)

    def _save_notes(self) -> None:
        if not self._doc_id:
            return
        content = self._editor.toPlainText()
        self.db.upsert_notes(self._doc_id, content)
        self.notes_saved.emit(self._doc_id)
        self.window().show_status("Notes saved")

    def _markdown_to_html(self, text: str) -> str:
        """Simple markdown to HTML conversion."""
        lines = text.split("\n")
        html_parts: list[str] = []
        html_parts.append(
            '<div style="font-family: Inter, sans-serif; line-height: 1.7; '
            'color: #F1F5F9; padding: 16px;">'
        )

        in_code = False
        for line in lines:
            if line.strip().startswith("```"):
                in_code = not in_code
                html_parts.append("<pre>" if in_code else "</pre>")
                continue

            if in_code:
                html_parts.append(f"<code>{self._escape(line)}</code><br>")
                continue

            if line.startswith("# "):
                html_parts.append(f"<h1 style='color: #F1F5F9;'>{self._escape(line[2:])}</h1>")
            elif line.startswith("## "):
                html_parts.append(f"<h2 style='color: #F1F5F9;'>{self._escape(line[3:])}</h2>")
            elif line.startswith("### "):
                html_parts.append(f"<h3 style='color: #F1F5F9;'>{self._escape(line[4:])}</h3>")
            elif line.startswith("- "):
                html_parts.append(f"<li>{self._escape(line[2:])}</li>")
            elif line.startswith("> "):
                html_parts.append(
                    f"<blockquote style='border-left: 3px solid #818CF8; "
                    f"padding-left: 12px; color: #94A3B8;'>{self._escape(line[2:])}</blockquote>"
                )
            elif line.strip():
                html_parts.append(f"<p>{self._escape(line)}</p>")
            else:
                html_parts.append("<br>")

        html_parts.append("</div>")
        return "\n".join(html_parts)

    @staticmethod
    def _escape(text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
