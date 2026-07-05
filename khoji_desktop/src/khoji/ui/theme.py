"""Theme management and QSS styling for Khoji.

Implements the design tokens from design/26-design-tokens.md.
"""

from __future__ import annotations

import json
from pathlib import Path


# ── Color Tokens ────────────────────────────────────────────────
DARK_THEME = {
    "bg_primary": "#0F172A",
    "bg_secondary": "#1E293B",
    "bg_tertiary": "#334155",
    "bg_hover": "#475569",
    "border": "#334155",
    "border_hover": "#475569",
    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_tertiary": "#64748B",
    "accent": "#818CF8",
    "accent_hover": "#6366F1",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "surface_card": "#1E293B",
    "surface_input": "#0F172A",
    "scrollbar_bg": "#1E293B",
    "scrollbar_thumb": "#475569",
    "selection": "#6366F140",
}

LIGHT_THEME = {
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F8FAFC",
    "bg_tertiary": "#F1F5F9",
    "bg_hover": "#E2E8F0",
    "border": "#E2E8F0",
    "border_hover": "#CBD5E1",
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "text_tertiary": "#94A3B8",
    "accent": "#6366F1",
    "accent_hover": "#4F46E5",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "surface_card": "#FFFFFF",
    "surface_input": "#F8FAFC",
    "scrollbar_bg": "#F1F5F9",
    "scrollbar_thumb": "#CBD5E1",
    "selection": "#6366F130",
}

SETTINGS_PATH = Path.home() / ".khoji" / "settings.json"


def load_theme_preference() -> str:
    if SETTINGS_PATH.exists():
        try:
            data = json.loads(SETTINGS_PATH.read_text())
            return data.get("theme", "dark")
        except Exception:
            pass
    return "dark"


def save_theme_preference(theme: str) -> None:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if SETTINGS_PATH.exists():
        try:
            data = json.loads(SETTINGS_PATH.read_text())
        except Exception:
            pass
    data["theme"] = theme
    SETTINGS_PATH.write_text(json.dumps(data, indent=2))


def get_theme_colors(theme_name: str) -> dict[str, str]:
    return DARK_THEME if theme_name == "dark" else LIGHT_THEME


def build_stylesheet(theme_name: str) -> str:
    """Generate full QSS stylesheet from design tokens."""
    c = get_theme_colors(theme_name)

    return f"""
    /* ── Global ─────────────────────────────────────────── */
    * {{
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        font-size: 14px;
        color: {c['text_primary']};
    }}

    QMainWindow, QWidget#centralWidget {{
        background-color: {c['bg_primary']};
    }}

    /* ── Sidebar ────────────────────────────────────────── */
    QWidget#sidebar {{
        background-color: {c['bg_secondary']};
        border-right: 1px solid {c['border']};
        min-width: 220px;
        max-width: 260px;
    }}

    QWidget#sidebar QPushButton {{
        text-align: left;
        padding: 10px 16px;
        border: none;
        border-radius: 8px;
        margin: 2px 8px;
        color: {c['text_secondary']};
        background: transparent;
        font-size: 13px;
    }}

    QWidget#sidebar QPushButton:hover {{
        background-color: {c['bg_tertiary']};
        color: {c['text_primary']};
    }}

    QWidget#sidebar QPushButton:checked {{
        background-color: {c['accent']}30;
        color: {c['accent']};
        font-weight: 600;
    }}

    QWidget#sidebar QLabel#sidebarTitle {{
        color: {c['text_tertiary']};
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 16px 16px 4px 16px;
    }}

    /* ── Work Area ──────────────────────────────────────── */
    QWidget#workArea {{
        background-color: {c['bg_primary']};
    }}

    /* ── Cards ──────────────────────────────────────────── */
    QFrame#card {{
        background-color: {c['surface_card']};
        border: 1px solid {c['border']};
        border-radius: 12px;
        padding: 16px;
    }}

    QFrame#card:hover {{
        border-color: {c['border_hover']};
    }}

    /* ── Buttons ────────────────────────────────────────── */
    QPushButton#primaryButton {{
        background-color: {c['accent']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 13px;
    }}

    QPushButton#primaryButton:hover {{
        background-color: {c['accent_hover']};
    }}

    QPushButton#primaryButton:disabled {{
        background-color: {c['bg_tertiary']};
        color: {c['text_tertiary']};
    }}

    QPushButton#secondaryButton {{
        background-color: transparent;
        color: {c['text_secondary']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 13px;
    }}

    QPushButton#secondaryButton:hover {{
        background-color: {c['bg_tertiary']};
        color: {c['text_primary']};
    }}

    QPushButton#dangerButton {{
        background-color: {c['error']}20;
        color: {c['error']};
        border: 1px solid {c['error']}40;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 13px;
    }}

    QPushButton#dangerButton:hover {{
        background-color: {c['error']}40;
    }}

    /* ── Inputs ─────────────────────────────────────────── */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {c['surface_input']};
        color: {c['text_primary']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 14px;
        selection-background-color: {c['accent']};
    }}

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {c['accent']};
    }}

    QLineEdit::placeholder {{
        color: {c['text_tertiary']};
    }}

    /* ── Scrollbars ─────────────────────────────────────── */
    QScrollBar:vertical {{
        background: {c['scrollbar_bg']};
        width: 8px;
        border-radius: 4px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background: {c['scrollbar_thumb']};
        border-radius: 4px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {c['text_tertiary']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}

    QScrollBar:horizontal {{
        background: {c['scrollbar_bg']};
        height: 8px;
        border-radius: 4px;
    }}

    QScrollBar::handle:horizontal {{
        background: {c['scrollbar_thumb']};
        border-radius: 4px;
        min-width: 30px;
    }}

    /* ── Status Bar ─────────────────────────────────────── */
    QStatusBar {{
        background-color: {c['bg_secondary']};
        border-top: 1px solid {c['border']};
        color: {c['text_tertiary']};
        font-size: 12px;
        padding: 2px 12px;
    }}

    /* ── Labels ─────────────────────────────────────────── */
    QLabel {{
        color: {c['text_primary']};
        background: transparent;
    }}

    QLabel#heading {{
        font-size: 24px;
        font-weight: 700;
        color: {c['text_primary']};
    }}

    QLabel#subheading {{
        font-size: 16px;
        font-weight: 600;
        color: {c['text_primary']};
    }}

    QLabel#muted {{
        color: {c['text_tertiary']};
        font-size: 13px;
    }}

    QLabel#accent {{
        color: {c['accent']};
        font-weight: 600;
    }}

    /* ── Badge ──────────────────────────────────────────── */
    QLabel#badge {{
        background-color: {c['accent']}20;
        color: {c['accent']};
        border-radius: 10px;
        padding: 2px 10px;
        font-size: 12px;
        font-weight: 600;
    }}

    QLabel#badgeSuccess {{
        background-color: {c['success']}20;
        color: {c['success']};
        border-radius: 10px;
        padding: 2px 10px;
        font-size: 12px;
        font-weight: 600;
    }}

    QLabel#badgeWarning {{
        background-color: {c['warning']}20;
        color: {c['warning']};
        border-radius: 10px;
        padding: 2px 10px;
        font-size: 12px;
        font-weight: 600;
    }}

    QLabel#badgeError {{
        background-color: {c['error']}20;
        color: {c['error']};
        border-radius: 10px;
        padding: 2px 10px;
        font-size: 12px;
        font-weight: 600;
    }}

    /* ── Splitter ───────────────────────────────────────── */
    QSplitter::handle {{
        background-color: {c['border']};
    }}

    QSplitter::handle:horizontal {{
        width: 1px;
    }}

    QSplitter::handle:vertical {{
        height: 1px;
    }}

    /* ── Progress Bar ───────────────────────────────────── */
    QProgressBar {{
        background-color: {c['bg_tertiary']};
        border: none;
        border-radius: 4px;
        height: 6px;
        text-align: center;
    }}

    QProgressBar::chunk {{
        background-color: {c['accent']};
        border-radius: 4px;
    }}

    /* ── Tab Widget ─────────────────────────────────────── */
    QTabWidget::pane {{
        border: 1px solid {c['border']};
        border-radius: 8px;
        background: {c['bg_primary']};
    }}

    QTabBar::tab {{
        background: transparent;
        color: {c['text_secondary']};
        padding: 8px 16px;
        border: none;
        font-size: 13px;
    }}

    QTabBar::tab:selected {{
        color: {c['accent']};
        font-weight: 600;
    }}

    QTabBar::tab:hover {{
        color: {c['text_primary']};
    }}

    /* ── Menu ───────────────────────────────────────────── */
    QMenu {{
        background-color: {c['bg_secondary']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 4px;
    }}

    QMenu::item {{
        padding: 8px 24px;
        border-radius: 4px;
    }}

    QMenu::item:selected {{
        background-color: {c['bg_tertiary']};
    }}

    /* ── ToolTip ────────────────────────────────────────── */
    QToolTip {{
        background-color: {c['bg_secondary']};
        color: {c['text_primary']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
    }}

    /* ── Chat Bubbles ───────────────────────────────────── */
    QFrame#chatBubbleUser {{
        background-color: {c['accent']}20;
        border: 1px solid {c['accent']}40;
        border-radius: 12px;
        padding: 12px;
    }}

    QFrame#chatBubbleAssistant {{
        background-color: {c['bg_secondary']};
        border: 1px solid {c['border']};
        border-radius: 12px;
        padding: 12px;
    }}

    /* ── Flashcard ──────────────────────────────────────── */
    QFrame#flashcard {{
        background-color: {c['surface_card']};
        border: 2px solid {c['border']};
        border-radius: 16px;
        padding: 32px;
        min-height: 200px;
    }}

    QFrame#flashcardCorrect {{
        border-color: {c['success']};
    }}

    QFrame#flashcardWrong {{
        border-color: {c['error']};
    }}

    /* ── Drop Zone ──────────────────────────────────────── */
    QFrame#dropZone {{
        background-color: {c['bg_secondary']};
        border: 2px dashed {c['border']};
        border-radius: 16px;
        padding: 48px;
    }}

    QFrame#dropZone:hover {{
        border-color: {c['accent']};
        background-color: {c['accent']}08;
    }}

    /* ── Empty State ────────────────────────────────────── */
    QWidget#emptyState {{
        background: transparent;
    }}

    QWidget#emptyState QLabel {{
        color: {c['text_tertiary']};
        font-size: 15px;
    }}
    """
