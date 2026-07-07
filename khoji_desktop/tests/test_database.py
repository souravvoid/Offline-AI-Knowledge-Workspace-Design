from __future__ import annotations

from pathlib import Path

import pytest

from khoji.database.db import Database


class TestDatabaseInit:
    def test_default_path(self):
        db = Database()
        assert db.db_path == Path.home() / ".khoji" / "khoji.db"
        db.close()

    def test_custom_path(self, tmp_db):
        assert tmp_db.db_path.suffix == ".db"
        assert tmp_db.db_path.parent.exists()

    def test_custom_str_path(self):
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            str_path = f.name
        db = Database(Path(str_path))
        assert db.db_path == Path(str_path)
        db.close()
        Path(str_path).unlink()

    def test_migration_creates_tables(self, tmp_db):
        tables = tmp_db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        names = [r["name"] for r in tables]
        assert "documents" in names
        assert "document_chunks" in names
        assert "notes" in names
        assert "flashcards" in names
        assert "quiz_questions" in names
        assert "chat_sessions" in names
        assert "chat_messages" in names


class TestDocuments:
    def test_create_and_get(self, tmp_db):
        doc = tmp_db.create_document(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            title="Test Doc",
            page_count=5,
        )
        assert doc["filename"] == "test.pdf"
        assert doc["title"] == "Test Doc"
        assert doc["page_count"] == 5
        assert doc["file_size"] == 1024
        assert doc["status"] == "uploaded"

        got = tmp_db.get_document(doc["id"])
        assert got is not None
        assert got["id"] == doc["id"]

    def test_get_nonexistent(self, tmp_db):
        assert tmp_db.get_document("nonexistent") is None

    def test_list_documents(self, tmp_db):
        tmp_db.create_document(filename="a.pdf", file_path="/a.pdf", file_size=100)
        tmp_db.create_document(filename="b.pdf", file_path="/b.pdf", file_size=200)
        docs = tmp_db.list_documents()
        assert len(docs) == 2

    def test_update_document(self, tmp_db):
        doc = tmp_db.create_document(filename="t.pdf", file_path="/t.pdf", file_size=100)
        updated = tmp_db.update_document(doc["id"], title="New Title", page_count=10)
        assert updated["title"] == "New Title"
        assert updated["page_count"] == 10

    def test_delete_document(self, tmp_db):
        doc = tmp_db.create_document(filename="d.pdf", file_path="/d.pdf", file_size=100)
        assert tmp_db.delete_document(doc["id"]) is True
        assert tmp_db.get_document(doc["id"]) is None

    def test_document_exists(self, tmp_db):
        tmp_db.create_document(filename="e.pdf", file_path="/e.pdf", file_size=100)
        found = tmp_db.document_exists("/e.pdf")
        assert found is not None
        not_found = tmp_db.document_exists("/missing.pdf")
        assert not_found is None


class TestChunks:
    def test_add_and_get_chunks(self, tmp_db):
        doc = tmp_db.create_document(filename="c.pdf", file_path="/c.pdf", file_size=100)
        chunks = [
            {"chunk_index": 0, "content": "Chunk one", "page_number": 1, "char_offset": 0, "char_length": 9},
            {"chunk_index": 1, "content": "Chunk two", "page_number": 1, "char_offset": 10, "char_length": 9},
        ]
        tmp_db.add_chunks(doc["id"], chunks)
        retrieved = tmp_db.get_chunks(doc["id"])
        assert len(retrieved) == 2
        assert retrieved[0]["content"] == "Chunk one"

    def test_search_chunks(self, tmp_db):
        doc = tmp_db.create_document(filename="s.pdf", file_path="/s.pdf", file_size=100)
        tmp_db.add_chunks(doc["id"], [
            {"chunk_index": 0, "content": "Machine learning is fun", "char_offset": 0, "char_length": 22},
            {"chunk_index": 1, "content": "Deep learning is cool", "char_offset": 23, "char_length": 20},
        ])
        results = tmp_db.search_chunks("learning")
        assert len(results) == 2

    def test_search_chunks_limit(self, tmp_db):
        doc = tmp_db.create_document(filename="l.pdf", file_path="/l.pdf", file_size=100)
        tmp_db.add_chunks(doc["id"], [
            {"chunk_index": i, "content": f"Item {i} with keyword", "char_offset": 0, "char_length": 20}
            for i in range(5)
        ])
        results = tmp_db.search_chunks("keyword", limit=2)
        assert len(results) == 2


class TestNotes:
    def test_upsert_notes_create(self, tmp_db):
        doc = tmp_db.create_document(filename="n.pdf", file_path="/n.pdf", file_size=100)
        result = tmp_db.upsert_notes(doc["id"], "Some notes")
        assert result is not None
        assert result["content"] == "Some notes"

    def test_upsert_notes_update(self, tmp_db):
        doc = tmp_db.create_document(filename="n2.pdf", file_path="/n2.pdf", file_size=100)
        tmp_db.upsert_notes(doc["id"], "Original")
        tmp_db.upsert_notes(doc["id"], "Updated")
        notes = tmp_db.get_notes(doc["id"])
        assert notes["content"] == "Updated"

    def test_get_notes_nonexistent(self, tmp_db):
        assert tmp_db.get_notes("nonexistent") is None


class TestFlashcards:
    def test_add_and_get_flashcards(self, tmp_db):
        doc = tmp_db.create_document(filename="f.pdf", file_path="/f.pdf", file_size=100)
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        tmp_db.add_flashcards(doc["id"], cards)
        retrieved = tmp_db.get_flashcards(doc["id"])
        assert len(retrieved) == 2

    def test_update_flashcard_review(self, tmp_db):
        doc = tmp_db.create_document(filename="fr.pdf", file_path="/fr.pdf", file_size=100)
        tmp_db.add_flashcards(doc["id"], [{"front": "Q", "back": "A"}])
        cards = tmp_db.get_flashcards(doc["id"])
        updated = tmp_db.update_flashcard_review(cards[0]["id"], quality=4)
        assert updated is not None
        assert updated["ease_factor"] >= 2.5

    def test_get_due_flashcards(self, tmp_db):
        doc = tmp_db.create_document(filename="fd.pdf", file_path="/fd.pdf", file_size=100)
        tmp_db.add_flashcards(doc["id"], [{"front": "Q", "back": "A"}])
        due = tmp_db.get_due_flashcards(doc["id"])
        assert len(due) == 1


class TestQuiz:
    def test_add_and_get_quiz(self, tmp_db):
        doc = tmp_db.create_document(filename="q.pdf", file_path="/q.pdf", file_size=100)
        questions = [
            {
                "question": "What is Python?",
                "options": ["Snake", "Language", "Both"],
                "correct_answer_index": 1,
                "explanation": "Python is a language",
            }
        ]
        tmp_db.add_quiz_questions(doc["id"], questions)
        retrieved = tmp_db.get_quiz_questions(doc["id"])
        assert len(retrieved) == 1
        assert retrieved[0]["options"] == ["Snake", "Language", "Both"]


class TestChat:
    def test_create_and_get_session(self, tmp_db):
        sess = tmp_db.create_chat_session("Test Chat")
        assert sess["title"] == "Test Chat"
        got = tmp_db.get_chat_session(sess["id"])
        assert got["id"] == sess["id"]

    def test_add_and_get_messages(self, tmp_db):
        sess = tmp_db.create_chat_session()
        msg = tmp_db.add_chat_message(sess["id"], "user", "Hello")
        assert msg["role"] == "user"
        messages = tmp_db.get_chat_messages(sess["id"])
        assert len(messages) == 1

    def test_list_sessions(self, tmp_db):
        doc = tmp_db.create_document(filename="cs.pdf", file_path="/cs.pdf", file_size=100)
        tmp_db.create_chat_session("Chat 1", doc["id"])
        tmp_db.create_chat_session("Chat 2", doc["id"])
        sessions = tmp_db.list_chat_sessions(doc["id"])
        assert len(sessions) == 2


class TestExportHelpers:
    def test_get_full_document_data(self, tmp_db):
        doc = tmp_db.create_document(filename="full.pdf", file_path="/full.pdf", file_size=100)
        data = tmp_db.get_full_document_data(doc["id"])
        assert data is not None
        assert data["id"] == doc["id"]
        assert data["chunks"] == []
        assert data["flashcards"] == []

    def test_get_full_document_data_missing(self, tmp_db):
        assert tmp_db.get_full_document_data("missing") is None


import tempfile
