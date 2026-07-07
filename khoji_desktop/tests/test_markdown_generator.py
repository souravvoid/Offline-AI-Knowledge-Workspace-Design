from __future__ import annotations

import pytest

from khoji.pipeline.markdown_generator import (
    generate_markdown,
    chunk_markdown,
    _is_heading,
    _is_list_item,
    _is_table_row,
    _split_into_paragraphs,
)


class TestGenerateMarkdown:
    def test_basic_markdown(self):
        md = generate_markdown("test.txt", "Hello world. This is a test.")
        assert "# test" in md
        assert "Source:" in md

    def test_custom_title(self):
        md = generate_markdown("file.txt", "Content", title="Custom")
        assert "# Custom" in md

    def test_page_count_included(self):
        md = generate_markdown("f.txt", "Content", page_count=5)
        assert "Pages: 5" in md

    def test_empty_text(self):
        md = generate_markdown("empty.txt", "")
        assert md is not None


class TestChunkMarkdown:
    def test_basic_chunking(self):
        text = "word " * 500
        chunks = chunk_markdown(text, chunk_size=200, overlap=50)
        assert len(chunks) > 0
        for c in chunks:
            assert "chunk_index" in c
            assert "content" in c
            assert "char_offset" in c
            assert "char_length" in c

    def test_empty_text(self):
        assert chunk_markdown("") == []

    def test_chunk_order(self):
        text = "word " * 1000
        chunks = chunk_markdown(text, chunk_size=300, overlap=50)
        indices = [c["chunk_index"] for c in chunks]
        assert indices == list(range(len(chunks)))


class TestIsHeading:
    def test_chapter_heading(self):
        assert _is_heading("Chapter 1 Introduction")

    def test_all_caps_heading(self):
        assert _is_heading("INTRODUCTION")

    def test_not_heading(self):
        assert not _is_heading("This is a regular sentence.")

    def test_short_uppercase_words(self):
        assert _is_heading("Data Structures")


class TestIsListItem:
    def test_dash_item(self):
        assert _is_list_item("- item")

    def test_asterisk_item(self):
        assert _is_list_item("* item")

    def test_not_list_item(self):
        assert not _is_list_item("normal text")


class TestIsTableRow:
    def test_has_pipe(self):
        assert _is_table_row("a | b | c")

    def test_no_pipe(self):
        assert not _is_table_row("normal text")

    def test_heading_not_table(self):
        assert not _is_table_row("# heading")


class TestSplitIntoParagraphs:
    def test_basic_split(self):
        text = "Para one.\n\nPara two.\n\nPara three."
        result = _split_into_paragraphs(text)
        assert len(result) == 3

    def test_single_para(self):
        result = _split_into_paragraphs("Just one paragraph.")
        assert len(result) == 1
