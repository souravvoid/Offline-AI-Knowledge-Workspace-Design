"""Flashcards view — spaced repetition study with flip animation."""

from __future__ import annotations

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from khoji.database.db import Database
from khoji.ui.animations import fade_in


class FlashcardWidget(QFrame):
    """Interactive flashcard with animated front/back flip."""

    def __init__(self, card: dict, parent=None) -> None:
        super().__init__(parent)
        self.card = card
        self._flipped = False
        self.setObjectName("flashcard")
        self.setMinimumHeight(250)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._stack = QFrame(self)
        stack_layout = QVBoxLayout(self._stack)
        stack_layout.setContentsMargins(32, 32, 32, 32)
        stack_layout.setSpacing(16)

        self._front_label = QLabel(card["front"])
        self._front_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._front_label.setWordWrap(True)
        self._front_label.setStyleSheet("font-size: 18px; font-weight: 500;")
        stack_layout.addWidget(self._front_label, 1)

        self._back_label = QLabel(card["back"])
        self._back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._back_label.setWordWrap(True)
        self._back_label.setStyleSheet("font-size: 16px;")
        self._back_label.setVisible(False)
        stack_layout.addWidget(self._back_label, 1)

        card_type = card.get("card_type", "basic")
        badge = QLabel(card_type.capitalize())
        badge.setObjectName("badge")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFixedWidth(70)
        stack_layout.addWidget(badge, 0, Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._stack, 1)

        self._front_opacity = QGraphicsOpacityEffect(self._front_label)
        self._back_opacity = QGraphicsOpacityEffect(self._back_label)
        self._front_label.setGraphicsEffect(self._front_opacity)
        self._back_label.setGraphicsEffect(self._back_opacity)

    def flip(self) -> None:
        self._flipped = not self._flipped

        if self._flipped:
            self._back_label.setVisible(True)
            self._animate_flip(self._front_opacity, 1.0, 0.0)
            QPropertyAnimation(
                self._back_opacity, b"opacity", self
            ).setDuration(300)
            fade_in(self._back_label, duration=300, delay=150)
        else:
            self._front_label.setVisible(True)
            self._animate_flip(self._back_opacity, 1.0, 0.0)
            fade_in(self._front_label, duration=300, delay=150)

    def _animate_flip(self, effect, start, end) -> None:
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(250)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.finished.connect(lambda: self._on_flip_done(effect, end))
        anim.start()

    def _on_flip_done(self, effect, value) -> None:
        if value == 0.0:
            if effect == self._front_opacity:
                self._front_label.setVisible(False)
            else:
                self._back_label.setVisible(False)

    def is_flipped(self) -> bool:
        return self._flipped


class FlashcardsView(QWidget):
    """Flashcards study panel with review controls."""

    def __init__(self, db: Database, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self._doc_id: str | None = None
        self._cards: list[dict] = []
        self._current_idx = 0
        self._card_widget: FlashcardWidget | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        self._title = QLabel("Flashcards")
        self._title.setObjectName("heading")
        header.addWidget(self._title)
        header.addStretch()

        self._counter = QLabel("0 / 0")
        self._counter.setObjectName("muted")
        header.addWidget(self._counter)
        layout.addLayout(header)

        # Card area
        self._card_container = QFrame()
        self._card_container.setObjectName("card")
        card_layout = QVBoxLayout(self._card_container)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._card_container, 1)

        # Controls
        controls = QHBoxLayout()
        controls.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._prev_btn = QPushButton("← Previous")
        self._prev_btn.setObjectName("secondaryButton")
        self._prev_btn.clicked.connect(self._prev_card)
        controls.addWidget(self._prev_btn)

        self._flip_btn = QPushButton("🔄  Flip")
        self._flip_btn.setObjectName("primaryButton")
        self._flip_btn.clicked.connect(self._flip_card)
        controls.addWidget(self._flip_btn)

        self._next_btn = QPushButton("Next →")
        self._next_btn.setObjectName("secondaryButton")
        self._next_btn.clicked.connect(self._next_card)
        controls.addWidget(self._next_btn)

        layout.addLayout(controls)

        # Difficulty buttons
        diff_layout = QHBoxLayout()
        diff_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for label, quality in [("❌ Again", 1), ("🤔 Hard", 3), ("✅ Good", 4), ("🎯 Easy", 5)]:
            btn = QPushButton(label)
            btn.setObjectName("secondaryButton")
            btn.clicked.connect(lambda checked, q=quality: self._rate(q))
            diff_layout.addWidget(btn)

        layout.addLayout(diff_layout)

        # Empty state
        self._empty = QLabel("No flashcards yet.\nUpload a document to generate flashcards.")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setObjectName("muted")
        # Success overlay
        self._success_overlay = QLabel("🎉  All cards reviewed!")
        self._success_overlay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._success_overlay.setStyleSheet("font-size: 18px; color: #10B981; font-weight: 600; padding: 48px;")
        self._success_overlay.setVisible(False)
        layout.addWidget(self._success_overlay)

        self._set_controls_enabled(False)

    def load_document(self, doc_id: str) -> None:
        self._doc_id = doc_id
        self._cards = self.db.get_flashcards(doc_id)
        self._current_idx = 0

        if self._cards:
            self._empty.setVisible(False)
            self._set_controls_enabled(True)
            self._show_card()
        else:
            self._empty.setVisible(True)
            self._set_controls_enabled(False)

        doc = self.db.get_document(doc_id)
        if doc:
            self._title.setText(f"Flashcards — {doc.get('title', doc['filename'])}")

    def _show_card(self) -> None:
        if not self._cards:
            return

        if self._card_widget:
            self._card_widget.deleteLater()

        card = self._cards[self._current_idx]
        self._card_widget = FlashcardWidget(card)

        layout = self._card_container.layout()
        layout.addWidget(self._card_widget)

        fade_in(self._card_widget, duration=300)

        self._counter.setText(f"{self._current_idx + 1} / {len(self._cards)}")

    def _flip_card(self) -> None:
        if self._card_widget:
            self._card_widget.flip()

    def _prev_card(self) -> None:
        if self._current_idx > 0:
            self._current_idx -= 1
            self._card_container.setGraphicsEffect(None)
            self._success_overlay.setVisible(False)
            self._show_card()

    def _next_card(self) -> None:
        if self._current_idx < len(self._cards) - 1:
            self._current_idx += 1
            self._card_container.setGraphicsEffect(None)
            self._success_overlay.setVisible(False)
            self._show_card()
        else:
            self._card_container.setVisible(False)
            self._success_overlay.setVisible(True)
            fade_in(self._success_overlay, duration=500)

    def _rate(self, quality: int) -> None:
        if not self._cards:
            return
        card = self._cards[self._current_idx]
        self.db.update_flashcard_review(card["id"], quality)
        self._next_card()

    def _set_controls_enabled(self, enabled: bool) -> None:
        self._prev_btn.setEnabled(enabled)
        self._flip_btn.setEnabled(enabled)
        self._next_btn.setEnabled(enabled)
