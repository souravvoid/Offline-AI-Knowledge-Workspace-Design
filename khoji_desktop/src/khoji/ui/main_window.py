"""Main application window for Khoji.

Layout: Sidebar | Work Area | StatusBar
All views are swapped into the work area.
"""

from __future__ import annotations


from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from khoji.database.db import Database
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

        # Sidebar
        self._sidebar = self._build_sidebar()
        root_layout.addWidget(self._sidebar)

        # Work area
        self._stack = QStackedWidget()
        self._stack.setObjectName("workArea")
        root_layout.addWidget(self._stack, 1)

        # Status bar
        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)
        self._status_label = QLabel("Ready")
        self._statusbar.addWidget(self._status_label, 1)

        self._progress_bar = QProgressBar()
        self._progress_bar.setMaximumWidth(200)
        self._progress_bar.setVisible(False)
        self._statusbar.addPermanentWidget(self._progress_bar)

        # Theme toggle
        self._theme_btn = QAction("🌙" if self._theme == "light" else "☀️", self)
        self._theme_btn.setShortcut(QKeySequence("Ctrl+Shift+T"))
        self._theme_btn.triggered.connect(self._toggle_theme)
        self._statusbar.addPermanentWidget(QLabel())  # spacer

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo
        logo_label = QLabel("  🔍 Khoji")
        logo_label.setStyleSheet("font-size: 18px; font-weight: 700; padding: 16px 12px;")
        layout.addWidget(logo_label)

        # Nav buttons
        self._nav_buttons: dict[str, QAction] = {}
        nav_items = [
            ("library", "📚  Library"),
            ("notes", "📝  Notes"),
            ("flashcards", "🃏  Flashcards"),
            ("quiz", "❓  Quiz"),
            ("chat", "💬  Chat"),
            ("search", "🔎  Search"),
        ]

        for key, label in nav_items:
            btn = self._make_nav_button(key, label)
            layout.addWidget(btn)

        layout.addStretch()

        # Settings
        settings_label = QLabel("  Settings")
        settings_label.setObjectName("sidebarTitle")
        layout.addWidget(settings_label)

        theme_btn = self._make_nav_button("theme", "🎨  Toggle Theme")
        layout.addWidget(theme_btn)

        return sidebar

    def _make_nav_button(self, key: str, label: str) -> QWidget:
        """Create a nav button that can hold an action."""
        from PySide6.QtWidgets import QPushButton

        btn = QPushButton(label)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.clicked.connect(lambda checked, k=key: self._on_nav(k))
        self._nav_buttons[key] = btn
        return btn

    def register_panel(self, name: str, panel: QWidget) -> None:
        """Register a view panel with the stack."""
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
        self._theme = "light" if self._theme == "dark" else "dark"
        save_theme_preference(self._theme)
        self._apply_theme()
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
            from PySide6.QtCore import QTimer

            QTimer.singleShot(timeout, lambda: self._status_label.setText("Ready"))

    def show_progress(self, visible: bool, value: int = 0) -> None:
        self._progress_bar.setVisible(visible)
        if visible:
            self._progress_bar.setValue(value)

    def get_theme(self) -> str:
        return self._theme
