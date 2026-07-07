from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from khoji.ui.theme import (
    DARK_THEME,
    LIGHT_THEME,
    load_theme_preference,
    save_theme_preference,
    get_theme_colors,
    build_stylesheet,
)


class TestThemeConstants:
    def test_dark_theme_keys(self):
        assert "bg_primary" in DARK_THEME
        assert "accent" in DARK_THEME
        assert "text_primary" in DARK_THEME

    def test_light_theme_keys(self):
        assert "bg_primary" in LIGHT_THEME
        assert "accent" in LIGHT_THEME

    def test_different_colors(self):
        assert DARK_THEME["bg_primary"] != LIGHT_THEME["bg_primary"]


class TestGetThemeColors:
    def test_dark(self):
        colors = get_theme_colors("dark")
        assert colors == DARK_THEME

    def test_light(self):
        colors = get_theme_colors("light")
        assert colors == LIGHT_THEME

    def test_default_to_light(self):
        colors = get_theme_colors("unknown")
        assert colors == LIGHT_THEME


class TestBuildStylesheet:
    def test_dark_stylesheet(self):
        ss = build_stylesheet("dark")
        assert "#0F172A" in ss
        assert "#818CF8" in ss

    def test_light_stylesheet(self):
        ss = build_stylesheet("light")
        assert "#FFFFFF" in ss
        assert "#6366F1" in ss


class TestLoadThemePreference:
    def test_no_settings_file(self):
        with patch("khoji.ui.theme.SETTINGS_PATH", Path("/nonexistent/settings.json")):
            assert load_theme_preference() == "dark"

    def test_with_settings_file(self, tmp_path):
        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"theme": "light"}))
        with patch("khoji.ui.theme.SETTINGS_PATH", settings):
            assert load_theme_preference() == "light"


class TestSaveThemePreference:
    def test_save_and_load(self, tmp_path):
        settings = tmp_path / "settings.json"
        with patch("khoji.ui.theme.SETTINGS_PATH", settings):
            save_theme_preference("light")
            assert json.loads(settings.read_text())["theme"] == "light"

    def test_overwrite_existing(self, tmp_path):
        settings = tmp_path / "settings.json"
        settings.write_text(json.dumps({"theme": "dark"}))
        with patch("khoji.ui.theme.SETTINGS_PATH", settings):
            save_theme_preference("light")
            assert json.loads(settings.read_text())["theme"] == "light"
