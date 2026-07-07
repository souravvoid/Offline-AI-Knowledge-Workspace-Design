from __future__ import annotations

from pathlib import Path

import pytest

from khoji.pipeline.pdf_extractor import (
    extract_pdf,
    extract_pdf_preview,
    get_page_count,
    _clean_extracted_text,
)


class TestExtractPdf:
    def test_extract_text(self, sample_pdf_path):
        result = extract_pdf(sample_pdf_path)
        assert result.page_count > 0
        assert "test PDF document" in result.full_text
        assert result.filename == sample_pdf_path.name

    def test_extract_preview(self, sample_pdf_path):
        preview = extract_pdf_preview(sample_pdf_path, max_pages=1)
        assert "test PDF document" in preview
        assert "Page 1" in preview

    def test_get_page_count(self, sample_pdf_path):
        count = get_page_count(sample_pdf_path)
        assert count > 0

    def test_nonexistent_file(self):
        result = extract_pdf("/nonexistent/file.pdf")
        assert len(result.errors) > 0
        assert result.page_count == 0


class TestCleanExtractedText:
    def test_remove_null_bytes(self):
        assert _clean_extracted_text("hello\x00world") == "helloworld"

    def test_collapse_spaces(self):
        assert _clean_extracted_text("hello    world") == "hello world"

    def test_collapse_newlines(self):
        assert _clean_extracted_text("hello\n\n\nworld") == "hello\n\nworld"

    def test_strip_whitespace(self):
        assert _clean_extracted_text("  hello  ") == "hello"
