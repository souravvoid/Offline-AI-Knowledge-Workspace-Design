from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from khoji.pipeline.ocr import (
    ocr_image,
    ocr_pdf_page,
    has_ocr_engine,
    _has_rapidocr,
    _clean_ocr_text,
    OcrResult,
)


class TestOcrResult:
    def test_dataclass(self):
        r = OcrResult(text="hello", confidence=0.9, engine="test")
        assert r.text == "hello"
        assert r.confidence == 0.9
        assert r.engine == "test"


class TestHasOcrEngine:
    def test_no_engine_available(self):
        with patch("khoji.pipeline.ocr._has_rapidocr", return_value=False):
            with patch("khoji.pipeline.ocr.shutil.which", return_value=None):
                assert has_ocr_engine() is False


class TestHasRapidOcr:
    def test_rapidocr_not_installed(self):
        assert _has_rapidocr() is False


class TestOcrImage:
    def test_no_engine(self):
        with patch("khoji.pipeline.ocr._try_rapidocr", return_value=None):
            with patch("khoji.pipeline.ocr._try_tesseract", return_value=None):
                result = ocr_image("/fake/path.png")
                assert result.text == ""
                assert result.engine == "none"

    def test_rapidocr_fallback_to_none(self):
        result = ocr_image("/nonexistent.png")
        assert isinstance(result, OcrResult)


class TestOcrPdfPage:
    def test_invalid_page(self):
        result = ocr_pdf_page("/fake.pdf", 999)
        assert result.engine == "error"

    def test_invalid_pdf(self):
        result = ocr_pdf_page("/nonexistent.pdf", 1)
        assert result.engine == "error"


class TestCleanOcrText:
    def test_collapse_whitespace(self):
        assert _clean_ocr_text("hello   world") == "hello world"

    def test_strip_whitespace(self):
        assert _clean_ocr_text("  hello  ") == "hello"
