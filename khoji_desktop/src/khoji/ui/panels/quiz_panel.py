"""Quiz view — multiple choice questions with scoring."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
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


class QuizQuestionWidget(QFrame):
    """Single quiz question with options."""

    answered = Signal(int, int)  # question_index, selected_option

    def __init__(self, question: dict, index: int, parent=None) -> None:
        super().__init__(parent)
        self.question = question
        self.index = index
        self._answered = False
        self._selected = -1
        self.setObjectName("card")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Difficulty badge
        diff = question.get("difficulty", "medium")
        badge = QLabel(diff.capitalize())
        badge.setObjectName(
            "badgeSuccess" if diff == "easy" else "badgeWarning" if diff == "medium" else "badgeError"
        )
        badge.setFixedWidth(60)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(badge, 0, Qt.AlignmentFlag.AlignLeft)

        # Question
        q_label = QLabel(f"Q{index + 1}. {question['question']}")
        q_label.setWordWrap(True)
        q_label.setStyleSheet("font-size: 16px; font-weight: 500;")
        layout.addWidget(q_label)

        # Options
        self._option_buttons: list[QPushButton] = []
        options = question.get("options", [])
        for i, option in enumerate(options):
            btn = QPushButton(f"  {option}")
            btn.setObjectName("secondaryButton")
            btn.setStyleSheet("text-align: left; padding: 12px 16px;")
            btn.clicked.connect(lambda checked, idx=i: self._select_option(idx))
            layout.addWidget(btn)
            self._option_buttons.append(btn)

        # Explanation (hidden until answered)
        self._explanation = QLabel("")
        self._explanation.setWordWrap(True)
        self._explanation.setObjectName("muted")
        self._explanation.setVisible(False)
        layout.addWidget(self._explanation)

    def _select_option(self, idx: int) -> None:
        if self._answered:
            return

        self._answered = True
        self._selected = idx
        correct = self.question.get("correct_answer_index", 0)

        for i, btn in enumerate(self._option_buttons):
            btn.setEnabled(False)
            if i == correct:
                btn.setStyleSheet(
                    "text-align: left; padding: 12px 16px; "
                    "background-color: #10B98130; border: 1px solid #10B98160; color: #10B981;"
                )
            elif i == idx and idx != correct:
                btn.setStyleSheet(
                    "text-align: left; padding: 12px 16px; "
                    "background-color: #EF444430; border: 1px solid #EF444460; color: #EF4444;"
                )

        explanation = self.question.get("explanation", "")
        if explanation:
            self._explanation.setText(f"💡 {explanation}")
            self._explanation.setVisible(True)

        self.answered.emit(self.index, idx)

    def was_correct(self) -> bool:
        return self._selected == self.question.get("correct_answer_index", -1)


class QuizView(QWidget):
    """Quiz panel with question cards and scoring."""

    def __init__(self, db: Database, parent=None) -> None:
        super().__init__(parent)
        self.db = db
        self._doc_id: str | None = None
        self._questions: list[dict] = []
        self._question_widgets: list[QuizQuestionWidget] = []
        self._answered_count = 0
        self._correct_count = 0
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        self._title = QLabel("Quiz")
        self._title.setObjectName("heading")
        header.addWidget(self._title)
        header.addStretch()

        self._score_label = QLabel("Score: 0 / 0")
        self._score_label.setObjectName("accent")
        header.addWidget(self._score_label)
        layout.addLayout(header)

        # Questions scroll
        from PySide6.QtWidgets import QScrollArea

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._questions_widget = QWidget()
        self._questions_layout = QVBoxLayout(self._questions_widget)
        self._questions_layout.setContentsMargins(0, 0, 0, 0)
        self._questions_layout.setSpacing(16)
        self._questions_layout.addStretch()

        self._scroll.setWidget(self._questions_widget)
        layout.addWidget(self._scroll, 1)

        # Empty state
        self._empty = QLabel("No quiz questions yet.\nUpload a document to generate questions.")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setObjectName("muted")
        layout.addWidget(self._empty)

    def load_document(self, doc_id: str) -> None:
        self._doc_id = doc_id
        self._questions = self.db.get_quiz_questions(doc_id)
        self._answered_count = 0
        self._correct_count = 0
        self._update_score()

        self._clear_questions()

        if self._questions:
            self._empty.setVisible(False)
            self._scroll.setVisible(True)

            for i, q in enumerate(self._questions):
                widget = QuizQuestionWidget(q, i)
                widget.answered.connect(self._on_answered)
                self._questions_layout.insertWidget(self._questions_layout.count() - 1, widget)
                self._question_widgets.append(widget)
        else:
            self._empty.setVisible(True)
            self._scroll.setVisible(False)

        doc = self.db.get_document(doc_id)
        if doc:
            self._title.setText(f"Quiz — {doc.get('title', doc['filename'])}")

    def _clear_questions(self) -> None:
        for w in self._question_widgets:
            w.deleteLater()
        self._question_widgets.clear()

    def _on_answered(self, index: int, selected: int) -> None:
        self._answered_count += 1
        widget = self._question_widgets[index]
        if widget.was_correct():
            self._correct_count += 1
        self._update_score()

    def _update_score(self) -> None:
        total = len(self._questions)
        self._score_label.setText(f"Score: {self._correct_count} / {self._answered_count} ({total} total)")
