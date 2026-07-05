"""Chat view — AI chat with streaming responses and context from documents."""

from __future__ import annotations


from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from khoji.database.db import Database


class ChatBubble(QFrame):
    """Styled chat message bubble."""

    def __init__(self, role: str, content: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("chatBubbleUser" if role == "user" else "chatBubbleAssistant")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        # Role label
        role_label = QLabel("You" if role == "user" else "Khoji")
        role_label.setObjectName("accent" if role == "assistant" else "muted")
        role_label.setStyleSheet("font-weight: 600; font-size: 12px;")
        layout.addWidget(role_label)

        # Content
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(content_label)


class ChatWorker(QThread):
    """Background thread for LLM inference."""

    chunk_ready = Signal(str)
    finished = Signal(str)

    def __init__(self, prompt: str, system: str = "") -> None:
        super().__init__()
        self.prompt = prompt
        self.system = system

    def run(self) -> None:
        try:
            from khoji.ai.llm import get_llm

            llm = get_llm()
            full_response = []
            for chunk in llm.generate_stream(self.prompt, system=self.system):
                full_response.append(chunk)
                self.chunk_ready.emit(chunk)
            self.finished.emit("".join(full_response))
        except Exception as e:
            self.finished.emit(f"[Error: {e}]")


class ChatView(QWidget):
    """Chat panel with message history and input."""

    def __init__(self, db: Database, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self._session_id: str | None = None
        self._doc_id: str | None = None
        self._is_generating = False
        self._worker: ChatWorker | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setStyleSheet("border-bottom: 1px solid #334155; padding: 12px 24px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 12, 24, 12)

        self._title = QLabel("💬  Chat")
        self._title.setObjectName("heading")
        header_layout.addWidget(self._title)
        header_layout.addStretch()

        new_chat_btn = QPushButton("➕  New Chat")
        new_chat_btn.setObjectName("secondaryButton")
        new_chat_btn.clicked.connect(self._new_chat)
        header_layout.addWidget(new_chat_btn)
        layout.addWidget(header)

        # Messages scroll
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._messages_widget = QWidget()
        self._messages_layout = QVBoxLayout(self._messages_widget)
        self._messages_layout.setContentsMargins(24, 16, 24, 16)
        self._messages_layout.setSpacing(12)
        self._messages_layout.addStretch()

        self._scroll.setWidget(self._messages_widget)
        layout.addWidget(self._scroll, 1)

        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet("border-top: 1px solid #334155; padding: 12px 24px;")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(24, 12, 24, 12)
        input_layout.setSpacing(12)

        self._input = QTextEdit()
        self._input.setPlaceholderText("Ask about your documents...")
        self._input.setMaximumHeight(100)
        self._input.setAcceptRichText(False)
        input_layout.addWidget(self._input, 1)

        send_btn = QPushButton("Send")
        send_btn.setObjectName("primaryButton")
        send_btn.setFixedWidth(80)
        send_btn.clicked.connect(self._send_message)
        input_layout.addWidget(send_btn, 0, Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(input_frame)

        # Welcome message
        self._add_welcome()

    def _add_welcome(self) -> None:
        welcome = ChatBubble(
            "assistant",
            "Hello! I'm Khoji, your offline AI assistant. "
            "Ask me anything about your uploaded documents, or start a conversation.",
        )
        self._messages_layout.insertWidget(0, welcome)

    def load_document(self, doc_id: str) -> None:
        self._doc_id = doc_id
        doc = self.db.get_document(doc_id)
        if doc:
            self._title.setText(f"💬  Chat — {doc.get('title', doc['filename'])}")

        sessions = self.db.list_chat_sessions(doc_id)
        if sessions:
            self._session_id = sessions[0]["id"]
            self._load_messages()
        else:
            self._new_chat()

    def _new_chat(self) -> None:
        title = "New Chat"
        if self._doc_id:
            doc = self.db.get_document(self._doc_id)
            if doc:
                title = f"Chat: {doc.get('title', doc['filename'])}"

        session = self.db.create_chat_session(title=title, doc_id=self._doc_id)
        self._session_id = session["id"]

        self._clear_messages()
        self._add_welcome()

    def _load_messages(self) -> None:
        if not self._session_id:
            return

        self._clear_messages()
        messages = self.db.get_chat_messages(self._session_id)

        for msg in messages:
            bubble = ChatBubble(msg["role"], msg["content"])
            self._messages_layout.insertWidget(self._messages_layout.count() - 1, bubble)

    def _clear_messages(self) -> None:
        while self._messages_layout.count() > 1:
            item = self._messages_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _send_message(self) -> None:
        text = self._input.toPlainText().strip()
        if not text or self._is_generating:
            return

        if not self._session_id:
            self._new_chat()

        # Add user message
        user_bubble = ChatBubble("user", text)
        self._messages_layout.insertWidget(self._messages_layout.count() - 1, user_bubble)
        self.db.add_chat_message(self._session_id, "user", text)
        self._input.clear()

        # Generate response
        self._is_generating = True
        self._placeholder = ChatBubble("assistant", "Thinking...")
        self._messages_layout.insertWidget(self._messages_layout.count() - 1, self._placeholder)
        self._scroll_to_bottom()

        # Build context
        system = "You are Khoji, an offline AI knowledge assistant. Answer based on the user's documents."
        if self._doc_id:
            notes = self.db.get_notes(self._doc_id)
            if notes:
                context = notes.get("content", "")[:3000]
                system += f"\n\nDocument context:\n{context}"

        self._worker = ChatWorker(text, system)
        self._worker.chunk_ready.connect(self._on_chunk)
        self._worker.finished.connect(self._on_finished)
        self._worker.start()

    def _on_chunk(self, chunk: str) -> None:
        if hasattr(self, "_placeholder") and self._placeholder:
            current = self._placeholder.findChild(QLabel)
            if current:
                current.setText(current.text() + chunk)
            self._scroll_to_bottom()

    def _on_finished(self, response: str) -> None:
        self._is_generating = False

        if self._placeholder:
            self._placeholder.deleteLater()

        if response:
            assistant_bubble = ChatBubble("assistant", response)
            self._messages_layout.insertWidget(self._messages_layout.count() - 1, assistant_bubble)
            self.db.add_chat_message(self._session_id, "assistant", response)

        self._scroll_to_bottom()

    def _scroll_to_bottom(self) -> None:
        sb = self._scroll.verticalScrollBar()
        sb.setValue(sb.maximum())
