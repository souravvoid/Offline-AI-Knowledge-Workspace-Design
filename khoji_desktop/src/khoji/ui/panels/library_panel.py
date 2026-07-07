"""Library view — document management with upload, grid/list, drag-drop."""

from __future__ import annotations


from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from khoji.database.db import Database
from khoji.pipeline.processor import ProcessingWorker
from khoji.ui.animations import fade_in


class DocumentCard(QFrame):
    """Card widget for a single document with stagger fade-in."""

    clicked = Signal(str)

    def __init__(self, doc: dict, parent=None, index: int = 0) -> None:
        super().__init__(parent)
        self.doc_id = doc["id"]
        self.setObjectName("card")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(140)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAccessibleName(f"Document Card: {doc.get('title', doc.get('filename', ''))}")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._index = index
        fade_in(self, duration=250, delay=index * 80)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(6)

        title = QLabel(doc.get("title", doc["filename"]))
        title.setObjectName("subheading")
        title.setWordWrap(True)
        layout.addWidget(title)

        meta_parts = []
        if doc.get("page_count"):
            meta_parts.append(f"{doc['page_count']} pages")
        if doc.get("file_size"):
            meta_parts.append(_format_size(doc["file_size"]))
        meta = QLabel(" · ".join(meta_parts) if meta_parts else doc["filename"])
        meta.setObjectName("muted")
        layout.addWidget(meta)

        status = doc.get("status", "uploaded")
        badge = QLabel(status.capitalize())
        badge.setObjectName(
            "badgeSuccess" if status == "processed" else "badgeWarning" if status == "processing" else "badge"
        )
        badge.setFixedWidth(80)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(badge)

        layout.addStretch()

    def mousePressEvent(self, event) -> None:
        self.clicked.emit(self.doc_id)
        super().mousePressEvent(event)


class LibraryView(QWidget):
    """Main library panel with document grid and upload."""

    document_selected = Signal(str)
    processing_started = Signal(str)
    processing_finished = Signal(str, bool)

    def __init__(self, db: Database, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self.setAcceptDrops(True)
        # Accessibility enhancements
        self.setAccessibleName("Library Panel")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        title = QLabel("Library")
        title.setObjectName("heading")
        header.addWidget(title)
        header.addStretch()

        upload_btn = QPushButton("📄  Upload Document")
        upload_btn.setObjectName("primaryButton")
        upload_btn.clicked.connect(self._upload_file)
        header.addWidget(upload_btn)
        layout.addLayout(header)

        # Empty state
        self._empty_state = QWidget()
        self._empty_state.setObjectName("emptyState")
        empty_layout = QVBoxLayout(self._empty_state)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        empty_icon = QLabel("📚")
        empty_icon.setStyleSheet("font-size: 48px;")
        empty_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(empty_icon)

        empty_text = QLabel("No documents yet.\nDrag & drop a PDF here, or click Upload.")
        empty_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_text.setObjectName("muted")
        empty_layout.addWidget(empty_text)

        layout.addWidget(self._empty_state)

        # Scroll area with cards
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setVisible(False)

        self._cards_widget = QWidget()
        self._cards_layout = QHBoxLayout(self._cards_widget)
        self._cards_layout.setContentsMargins(0, 0, 0, 0)
        self._cards_layout.setSpacing(16)
        self._cards_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._scroll.setWidget(self._cards_widget)
        layout.addWidget(self._scroll, 1)

    def refresh(self) -> None:
        """Reload document list from DB."""
        docs = self.db.list_documents()
        self._clear_cards()

        if not docs:
            self._empty_state.setVisible(True)
            self._scroll.setVisible(False)
            return

        self._empty_state.setVisible(False)
        self._scroll.setVisible(True)

        for i, doc in enumerate(docs):
            card = DocumentCard(doc, index=i)
            card.clicked.connect(self.document_selected.emit)
            self._cards_layout.addWidget(card)

        self._cards_layout.addStretch()

    def _clear_cards(self) -> None:
        while self._cards_layout.count():
            item = self._cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _upload_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Upload Document",
            "",
            "PDF Files (*.pdf);;All Files (*)",
        )
        if file_path:
            self._start_processing(file_path)

    def _start_processing(self, file_path: str) -> None:
        self.processing_started.emit(file_path)
        worker = ProcessingWorker(file_path, self.db)
        worker.finished.connect(self._on_processing_done)
        worker.progress.connect(lambda msg: self.window().show_status(msg, 0))
        worker.start()
        self._current_worker = worker

    @Slot(object)
    def _on_processing_done(self, result) -> None:
        self.processing_finished.emit(result.doc_id, result.success)
        if result.success:
            self.window().show_status(f"Processed: {result.message}")
        else:
            self.window().show_status(f"Error: {result.message}")
        self.refresh()

    # ── Drag & Drop ────────────────────────────────────────────
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            self._show_drop_zone()
            event.acceptProposedAction()

    def dragLeaveEvent(self, event) -> None:
        self._hide_drop_zone()
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".pdf"):
                self._start_processing(path)
                break


    def _show_drop_zone(self) -> None:
        if not hasattr(self, "_drop_overlay"):
            self._drop_overlay = QFrame(self)
            self._drop_overlay.setObjectName("dropZone")
            self._drop_overlay.setGeometry(self.rect())
            drop_layout = QVBoxLayout(self._drop_overlay)
            drop_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            drop_layout.setSpacing(12)

            icon = QLabel("📄")
            icon.setStyleSheet("font-size: 48px;")
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            drop_layout.addWidget(icon)

            text = QLabel("Drop your document here")
            text.setStyleSheet("font-size: 16px; color: #818CF8; font-weight: 600;")
            text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            drop_layout.addWidget(text)

            sub = QLabel("Supports PDF files")
            sub.setStyleSheet("font-size: 12px; color: #64748B;")
            sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
            drop_layout.addWidget(sub)

        self._drop_overlay.setVisible(True)
        self._drop_overlay.raise_()
        fade_in(self._drop_overlay, duration=200)

    def _hide_drop_zone(self) -> None:
        if hasattr(self, "_drop_overlay"):
            self._drop_overlay.setVisible(False)


def _format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
