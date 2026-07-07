"""Main application window for Khoji.

Layout: Sidebar | Work Area | StatusBar
All views are swapped into the work area.
"""

from __future__ import annotations


from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from khoji.database.db import Database
from khoji.ui.animations import fade_in
from khoji.ui.theme import build_stylesheet, load_theme_preference, save_theme_preference


class MainWindow(QMainWindow):
    """Top-level window. Sidebar navigation + stacked work area."""

    theme_changed = Signal(str)

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self._theme = load_theme_preference()
        self._panels: dict[str, QWidget] = {}
        self._panel_names: list[str] = []
        self._sidebar_collapsed = False
        self._sidebar_full_width = 240
        self._sidebar_mini_width = 68

        self.setWindowTitle("Khoji — Offline AI Knowledge Workspace")
        self.setMinimumSize(1100, 700)
        self.resize(1400, 900)

        self._build_ui()
        self._apply_theme()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self._sidebar = self._build_sidebar()
        root_layout.addWidget(self._sidebar)

        self._stack = QStackedWidget()
        self._stack.setObjectName("workArea")
        root_layout.addWidget(self._stack, 1)

        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)
        self._status_label = QLabel("Ready")
        self._statusbar.addWidget(self._status_label, 1)

        self._progress_bar = QProgressBar()
        self._progress_bar.setMaximumWidth(200)
        self._progress_bar.setVisible(False)
        self._statusbar.addPermanentWidget(self._progress_bar)

        self._theme_btn = QAction("🌙" if self._theme == "light" else "☀️", self)
        self._theme_btn.setShortcut(QKeySequence("Ctrl+Shift+T"))
        self._theme_btn.triggered.connect(self._toggle_theme)
        self._statusbar.addPermanentWidget(QLabel())

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(self._sidebar_full_width)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo_label = QLabel("  🔍 Khoji")
        logo_label.setObjectName("sidebarLogo")
        logo_label.setStyleSheet("font-size: 18px; font-weight: 700; padding: 16px 12px;")
        layout.addWidget(logo_label)

        # Collapse toggle button
        self._collapse_btn = QPushButton("◀  Collapse")
        self._collapse_btn.setStyleSheet(
            "text-align: left; padding: 8px 16px; border: none;"
            "color: #64748B; font-size: 12px; background: transparent;"
        )
        self._collapse_btn.clicked.connect(self._toggle_sidebar)
        layout.addWidget(self._collapse_btn)

        self._nav_labels: dict[str, QLabel] = {}
        self._nav_buttons: dict[str, QPushButton] = {}
        nav_items = [
            ("library", "📚", "Library"),
            ("notes", "📝", "Notes"),
            ("flashcards", "🃏", "Flashcards"),
            ("quiz", "❓", "Quiz"),
            ("chat", "💬", "Chat"),
            ("search", "🔎", "Search"),
        ]

        for key, icon, label in nav_items:
            btn, label_widget = self._make_nav_button(key, icon, label)
            layout.addWidget(btn)
            self._nav_labels[key] = label_widget

        layout.addStretch()

        settings_label = QLabel("  Settings")
        settings_label.setObjectName("sidebarTitle")
        layout.addWidget(settings_label)

        theme_btn, _ = self._make_nav_button("theme", "🎨", "Toggle Theme")
        layout.addWidget(theme_btn)

        return sidebar

    def _make_nav_button(self, key: str, icon: str, label: str) -> tuple:
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setFixedHeight(44)
        btn.clicked.connect(lambda checked, k=key: self._on_nav(k))

        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(12, 0, 12, 0)
        btn_layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 16px;")
        btn_layout.addWidget(icon_label)

        text_label = QLabel(label)
        text_label.setStyleSheet("font-size: 13px;")
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()

        self._nav_buttons[key] = btn
        return btn, text_label

    def _toggle_sidebar(self) -> None:
        self._sidebar_collapsed = not self._sidebar_collapsed
        target_width = self._sidebar_mini_width if self._sidebar_collapsed else self._sidebar_full_width

        anim = QPropertyAnimation(self._sidebar, b"minimumWidth")
        anim.setDuration(220)
        anim.setStartValue(self._sidebar.width())
        anim.setEndValue(target_width)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()

        anim2 = QPropertyAnimation(self._sidebar, b"maximumWidth")
        anim2.setDuration(220)
        anim2.setStartValue(self._sidebar.width())
        anim2.setEndValue(target_width)
        anim2.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim2.start()

        self._collapse_btn.setText("▶" if self._sidebar_collapsed else "◀  Collapse")
        for label in self._nav_labels.values():
            label.setVisible(not self._sidebar_collapsed)

    def register_panel(self, name: str, panel: QWidget) -> None:
        self._panels[name] = panel
        self._stack.addWidget(panel)
        self._panel_names.append(name)

    def _on_nav(self, key: str) -> None:
        if key == "theme":
            self._toggle_theme()
            return
        if key in self._panels:
            self._stack.setCurrentWidget(self._panels[key])
            self._status_label.setText(key.capitalize())

    def _toggle_theme(self) -> None:
        new_theme = "light" if self._theme == "dark" else "dark"
        overlay = QWidget(self)
        overlay.setStyleSheet(f"background-color: {'#0F172A' if new_theme == 'dark' else '#FFFFFF'};")
        overlay.setGeometry(self.rect())
        overlay.raise_()

        eff = QGraphicsOpacityEffect(overlay)
        overlay.setGraphicsEffect(eff)
        eff.setOpacity(0.0)
        overlay.show()

        fade_anim = QPropertyAnimation(eff, b"opacity")
        fade_anim.setDuration(250)
        fade_anim.setStartValue(0.0)
        fade_anim.setEndValue(1.0)
        fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        fade_anim.finished.connect(lambda: self._finish_theme_switch(new_theme, overlay))
        fade_anim.start()

    def _finish_theme_switch(self, new_theme: str, overlay: QWidget) -> None:
        self._theme = new_theme
        save_theme_preference(self._theme)
        self._apply_theme()
        overlay.deleteLater()
        self.theme_changed.emit(self._theme)

    def _apply_theme(self) -> None:
        app = QApplication.instance()
        if app:
            app.setStyleSheet(build_stylesheet(self._theme))

    def _connect_signals(self) -> None:
        pass

    def show_status(self, message: str, timeout: int = 5000) -> None:
        self._status_label.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self._status_label.setText("Ready"))

    def show_progress(self, visible: bool, value: int = 0) -> None:
        self._progress_bar.setVisible(visible)
        if visible:
            self._progress_bar.setValue(value)

    def get_theme(self) -> str:
        return self._theme
