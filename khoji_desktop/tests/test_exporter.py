from __future__ import annotations

import json

import pytest

from khoji.pipeline.exporter import (
    export_markdown,
    export_flashcards_anki,
    export_quiz_json,
    export_full_json,
    export_all_documents_csv,
)


class TestExportMarkdown:
    def test_export_with_notes(self, tmp_db):
        doc = tmp_db.create_document(filename="test.pdf", file_path="/t.pdf", file_size=100)
        tmp_db.upsert_notes(doc["id"], "# My Notes\nContent here")
        md = export_markdown(doc["id"], tmp_db)
        assert "# My Notes" in md

    def test_export_without_notes(self, tmp_db):
        doc = tmp_db.create_document(filename="test.pdf", file_path="/t2.pdf", file_size=100)
        md = export_markdown(doc["id"], tmp_db)
        assert "No notes generated" in md

    def test_export_missing_doc(self, tmp_db):
        assert export_markdown("missing", tmp_db) == ""


class TestExportFlashcardsAnki:
    def test_export_anki(self, tmp_db):
        doc = tmp_db.create_document(filename="f.pdf", file_path="/f.pdf", file_size=100)
        tmp_db.add_flashcards(doc["id"], [
            {"front": "Question 1", "back": "Answer 1"},
        ])
        result = export_flashcards_anki(doc["id"], tmp_db)
        assert "Question 1" in result
        assert "Answer 1" in result

    def test_export_empty(self, tmp_db):
        assert export_flashcards_anki("missing", tmp_db) == ""


class TestExportQuizJson:
    def test_export_quiz(self, tmp_db):
        doc = tmp_db.create_document(filename="q.pdf", file_path="/q.pdf", file_size=100)
        tmp_db.add_quiz_questions(doc["id"], [
            {
                "question": "What is X?",
                "options": ["A", "B", "C"],
                "correct_answer_index": 0,
            },
        ])
        result = json.loads(export_quiz_json(doc["id"], tmp_db))
        assert len(result) == 1
        assert result[0]["question"] == "What is X?"

    def test_export_empty(self, tmp_db):
        assert export_quiz_json("missing", tmp_db) == "[]"


class TestExportFullJson:
    def test_export_full(self, tmp_db):
        doc = tmp_db.create_document(filename="full.pdf", file_path="/full.pdf", file_size=100)
        doc2 = tmp_db.get_document(doc["id"])
        result = json.loads(export_full_json(doc["id"], tmp_db))
        assert result["filename"] == "full.pdf"

    def test_export_missing(self, tmp_db):
        assert export_full_json("missing", tmp_db) == "{}"


class TestExportAllDocumentsCsv:
    def test_export_csv(self, tmp_db):
        tmp_db.create_document(filename="a.pdf", file_path="/a.pdf", file_size=100)
        csv_out = export_all_documents_csv(tmp_db)
        assert "Filename" in csv_out
        assert "a.pdf" in csv_out

    def test_export_empty_db(self, tmp_db):
        from khoji.database.db import Database
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            empty_db = Database(Path(tmp) / "empty.db")
            assert export_all_documents_csv(empty_db) == ""
            empty_db.close()
