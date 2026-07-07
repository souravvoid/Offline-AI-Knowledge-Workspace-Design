from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SplashScreen(QWidget):
    """Animated splash screen that initializes local AI models."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("splashScreen")
        self.setStyleSheet("""
            #splashScreen {
                background-color: #0F172A;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(24)

        layout.addStretch(2)

        # Logo
        self._logo = QLabel("🔍")
        self._logo.setStyleSheet("font-size: 64px;")
        self._logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._logo)

        # Title
        self._title = QLabel("Khoji")
        self._title.setStyleSheet("font-size: 36px; font-weight: 700; color: #F1F5F9;")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._title)

        # Subtitle
        self._subtitle = QLabel("Offline AI Knowledge Workspace")
        self._subtitle.setStyleSheet("font-size: 14px; color: #64748B;")
        self._subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._subtitle)

        layout.addStretch(1)

        # Status message
        self._status = QLabel("Initializing...")
        self._status.setStyleSheet("font-size: 13px; color: #94A3B8;")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)

        # Loading bar
        bar_frame = QWidget()
        bar_frame.setFixedWidth(240)
        bar_layout = QVBoxLayout(bar_frame)
        bar_layout.setContentsMargins(0, 0, 0, 0)

        self._progress = QProgressBar()
        self._progress.setFixedHeight(3)
        self._progress.setRange(0, 100)
        self._progress.setTextVisible(False)
        self._progress.setStyleSheet("""
            QProgressBar {
                background-color: #1E293B;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #818CF8;
                border-radius: 2px;
            }
        """)
        bar_layout.addWidget(self._progress)
        layout.addWidget(bar_frame, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addStretch(2)

        self._status_messages = [
            ("Initializing...", 0),
            ("Loading AI Models...", 20),
            ("Preparing Embeddings...", 40),
            ("Configuring LLM...", 60),
            ("Loading Knowledge Base...", 80),
            ("Ready!", 100),
        ]
        self._msg_index = 0
        self._start_animation()

    def _start_animation(self) -> None:
        # Logo scale animation
        self._logo_anim = QPropertyAnimation(self._logo, b"geometry")
        self._logo_anim.setDuration(2000)
        self._logo_anim.setStartValue(self._logo.geometry())
        self._logo_anim.setEndValue(self._logo.geometry())
        self._logo_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        self._logo_anim.start()

        # Progress simulation
        self._animate_progress()

    def _animate_progress(self) -> None:
        if self._msg_index >= len(self._status_messages):
            return

        msg, value = self._status_messages[self._msg_index]
        self._status.setText(msg)

        anim = QPropertyAnimation(self._progress, b"value")
        anim.setDuration(800)
        anim.setStartValue(self._progress.value())
        anim.setEndValue(value)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.finished.connect(self._on_progress_step)
        anim.start()

    def _on_progress_step(self) -> None:
        self._msg_index += 1
        if self._msg_index < len(self._status_messages):
            QTimer.singleShot(300, self._animate_progress)
        else:
            QTimer.singleShot(500, self.close)

    def close(self) -> None:
        self.setGraphicsEffect(None)
        self.parent().splash_finished()


class SplashOverlay(QWidget):
    """Overlay that covers the main window during startup."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("splashOverlay")
        self.setStyleSheet("""
            #splashOverlay {
                background-color: #0F172A;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)

        self._logo = QLabel("🔍")
        self._logo.setStyleSheet("font-size: 48px;")
        self._logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._logo)

        self._status = QLabel("Loading AI Models...")
        self._status.setStyleSheet("font-size: 14px; color: #94A3B8;")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)

    def set_status(self, message: str) -> None:
        self._status.setText(message)
