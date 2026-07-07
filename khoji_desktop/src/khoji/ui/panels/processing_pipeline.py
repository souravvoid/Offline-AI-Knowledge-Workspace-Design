from __future__ import annotations

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from khoji.ui.animations import fade_in


PIPELINE_STEPS = [
    ("📄", "Import", "Importing document..."),
    ("🔍", "OCR", "Running OCR..."),
    ("📝", "Extract Text", "Extracting text..."),
    ("✂️", "Chunk", "Chunking text..."),
    ("🧠", "Embedding", "Generating embeddings..."),
    ("🤖", "LLM", "Running AI analysis..."),
    ("📋", "Markdown", "Creating markdown..."),
    ("❓", "Quiz", "Generating quiz..."),
    ("🃏", "Flashcards", "Creating flashcards..."),
    ("✅", "Done", "Processing complete!"),
]


class PipelineStep(QFrame):
    """A single step in the processing pipeline."""

    def __init__(self, icon: str, label: str, description: str, index: int, parent=None) -> None:
        super().__init__(parent)
        self._index = index
        self._completed = False
        self._current = False

        self.setFixedHeight(48)
        self.setStyleSheet("""
            PipelineStep {
                background: transparent;
                border: none;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(12)

        # Step number
        self._num = QLabel(str(index + 1))
        self._num.setFixedSize(28, 28)
        self._num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._num.setStyleSheet("""
            font-size: 12px; font-weight: 600;
            background-color: #334155; color: #64748B;
            border-radius: 14px;
        """)
        layout.addWidget(self._num)

        # Icon + Label
        self._icon = QLabel(icon)
        self._icon.setStyleSheet("font-size: 16px;")
        layout.addWidget(self._icon)

        self._label = QLabel(label)
        self._label.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 500;")
        layout.addWidget(self._label, 1)

        # Description
        self._desc = QLabel(description)
        self._desc.setStyleSheet("font-size: 11px; color: #475569;")
        self._desc.setVisible(False)
        layout.addWidget(self._desc)

        # Connector line
        self._line = QFrame()
        self._line.setFixedWidth(2)
        self._line.setStyleSheet("background-color: #1E293B; border-radius: 1px;")

    def set_current(self, current: bool) -> None:
        self._current = current
        if current:
            self._num.setStyleSheet("""
                font-size: 12px; font-weight: 600;
                background-color: #818CF8; color: white;
                border-radius: 14px;
            """)
            self._icon.setStyleSheet("font-size: 16px;")
            self._label.setStyleSheet("font-size: 13px; color: #F1F5F9; font-weight: 600;")
            self._desc.setVisible(True)

    def set_completed(self, completed: bool) -> None:
        self._completed = completed
        if completed:
            self._num.setStyleSheet("""
                font-size: 12px; font-weight: 600;
                background-color: #10B981; color: white;
                border-radius: 14px;
            """)
            self._label.setStyleSheet("font-size: 13px; color: #10B981; font-weight: 500;")

    def reset(self) -> None:
        self._completed = False
        self._current = False
        self._desc.setVisible(False)
        self._num.setStyleSheet("""
            font-size: 12px; font-weight: 600;
            background-color: #334155; color: #64748B;
            border-radius: 14px;
        """)
        self._label.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 500;")


class ProcessingPipeline(QWidget):
    """Visual processing pipeline with animated step transitions."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("processingPipeline")
        self.setFixedWidth(320)
        self.setStyleSheet("""
            #processingPipeline {
                background-color: #1E293B;
                border-radius: 12px;
                border: 1px solid #334155;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)

        # Title
        title = QLabel("Processing Pipeline")
        title.setStyleSheet("font-size: 14px; font-weight: 600; color: #F1F5F9;")
        layout.addWidget(title)

        subtitle = QLabel("Real-time document processing")
        subtitle.setStyleSheet("font-size: 11px; color: #64748B; margin-bottom: 12px;")
        layout.addWidget(subtitle)

        # Steps
        self._steps: list[PipelineStep] = []
        for i, (icon, label, desc) in enumerate(PIPELINE_STEPS):
            step = PipelineStep(icon, label, desc, i)
            self._steps.append(step)
            layout.addWidget(step)

        # Overall progress
        self._progress = QProgressBar()
        self._progress.setFixedHeight(4)
        self._progress.setRange(0, 100)
        self._progress.setTextVisible(False)
        self._progress.setStyleSheet("""
            QProgressBar {
                background-color: #0F172A;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #818CF8;
                border-radius: 2px;
            }
        """)
        layout.addWidget(self._progress)

        self._current_step = -1
        self._is_active = False
        self.setVisible(False)

    def start(self) -> None:
        self._is_active = True
        self._current_step = -1
        for s in self._steps:
            s.reset()
        self._progress.setValue(0)
        self.setVisible(True)
        fade_in(self, duration=300)
        QTimer.singleShot(400, self._advance_step)

    def _advance_step(self) -> None:
        if not self._is_active:
            return

        if self._current_step >= 0 and self._current_step < len(self._steps):
            self._steps[self._current_step].set_completed(True)

        self._current_step += 1

        if self._current_step >= len(self._steps):
            self._is_active = False
            QTimer.singleShot(1500, self._finish)
            return

        self._steps[self._current_step].set_current(True)
        progress_value = int((self._current_step + 1) / len(self._steps) * 100)

        anim = QPropertyAnimation(self._progress, b"value")
        anim.setDuration(400)
        anim.setStartValue(self._progress.value())
        anim.setEndValue(progress_value)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()

        QTimer.singleShot(1200, self._advance_step)

    def _finish(self) -> None:
        for s in self._steps:
            s.set_completed(True)
        self._progress.setValue(100)

    def stop(self) -> None:
        self._is_active = False
        self.setVisible(False)
