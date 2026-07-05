"""Search view — semantic search across all documents with results display."""

from __future__ import annotations

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from khoji.database.db import Database


class SearchResultCard(QFrame):
    """Single search result card."""

    def __init__(self, result: dict, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        # Source and score
        source = result.get("filename", result.get("title", "Unknown"))
        score = result.get("score", 0)
        header = QHBoxLayout()
        src_label = QLabel(f"📄  {source}")
        src_label.setObjectName("muted")
        header.addWidget(src_label)
        header.addStretch()

        if score:
            score_label = QLabel(f"Score: {score:.2f}")
            score_label.setObjectName("badge")
            header.addWidget(score_label)
        layout.addLayout(header)

        # Content preview
        content = result.get("content", "")
        preview = content[:300] + "..." if len(content) > 300 else content
        preview_label = QLabel(preview)
        preview_label.setWordWrap(True)
        preview_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(preview_label, 1)


class SearchWorker(QThread):
    """Background thread for semantic search."""

    results_ready = Signal(list)

    def __init__(self, query: str, db: Database) -> None:
        super().__init__()
        self.query = query
        self.db = db

    def run(self) -> None:
        results: list[dict] = []

        # Try vector search first
        try:
            from khoji.ai.vector_search import get_vector_store

            store = get_vector_store()
            vector_results = store.search(self.query, limit=20)

            for vr in vector_results:
                meta = vr.get("metadata", {})
                doc_id = meta.get("document_id", "")

                if doc_id:
                    doc = self.db.get_document(doc_id)
                    if doc:
                        results.append({
                            "filename": doc.get("filename", ""),
                            "title": doc.get("title", ""),
                            "content": f"Chunk {meta.get('chunk_index', '?')}",
                            "score": vr.get("score", 0),
                        })
        except Exception:
            pass

        # Fallback to text search
        if not results:
            text_results = self.db.search_chunks(self.query, limit=20)
            for r in text_results:
                results.append({
                    "filename": r.get("filename", ""),
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "score": 0,
                })

        self.results_ready.emit(results)


class SearchView(QWidget):
    """Search panel with query input and results display."""

    def __init__(self, db: Database, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self._worker: SearchWorker | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        title = QLabel("Search")
        title.setObjectName("heading")
        layout.addWidget(title)

        # Search input
        search_frame = QFrame()
        search_frame.setObjectName("card")
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(16, 8, 8, 8)
        search_layout.setSpacing(8)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search across all documents...")
        self._search_input.returnPressed.connect(self._do_search)
        search_layout.addWidget(self._search_input, 1)

        search_btn = QPushButton("🔎  Search")
        search_btn.setObjectName("primaryButton")
        search_btn.clicked.connect(self._do_search)
        search_layout.addWidget(search_btn)
        layout.addWidget(search_frame)

        # Results count
        self._count_label = QLabel("")
        self._count_label.setObjectName("muted")
        layout.addWidget(self._count_label)

        # Results scroll
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._results_widget = QWidget()
        self._results_layout = QVBoxLayout(self._results_widget)
        self._results_layout.setContentsMargins(0, 0, 0, 0)
        self._results_layout.setSpacing(12)
        self._results_layout.addStretch()

        self._scroll.setWidget(self._results_widget)
        layout.addWidget(self._scroll, 1)

        # Empty state
        self._empty = QLabel("Type a query to search across all your documents.")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setObjectName("muted")
        layout.addWidget(self._empty)

    def _do_search(self) -> None:
        query = self._search_input.text().strip()
        if not query:
            return

        self._count_label.setText("Searching...")
        self._clear_results()

        self._worker = SearchWorker(query, self.db)
        self._worker.results_ready.connect(self._show_results)
        self._worker.start()

    def _show_results(self, results: list[dict]) -> None:
        self._clear_results()

        if not results:
            self._count_label.setText("No results found.")
            self._empty.setVisible(True)
            self._scroll.setVisible(False)
            return

        self._empty.setVisible(False)
        self._scroll.setVisible(True)
        self._count_label.setText(f"{len(results)} results")

        for r in results:
            card = SearchResultCard(r)
            self._results_layout.insertWidget(self._results_layout.count() - 1, card)

    def _clear_results(self) -> None:
        while self._results_layout.count() > 1:
            item = self._results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
