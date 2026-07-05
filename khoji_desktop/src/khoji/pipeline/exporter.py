"""Export system — markdown, Anki, JSON, CSV formats.

Port of the Rust export commands from commands.rs.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

from khoji.database.db import Database


def export_markdown(doc_id: str, db: Database) -> str:
    """Export document notes as clean Markdown."""
    data = db.get_full_document_data(doc_id)
    if not data:
        return ""

    notes = data.get("notes")
    if notes and notes.get("content"):
        return notes["content"]

    return f"# {data.get('title', data['filename'])}\n\nNo notes generated yet."


def export_flashcards_anki(doc_id: str, db: Database) -> str:
    """Export flashcards in Anki-compatible tab-separated format."""
    cards = db.get_flashcards(doc_id)
    if not cards:
        return ""

    lines = []
    for card in cards:
        front = card["front"].replace("\t", " ").replace("\n", " ")
        back = card["back"].replace("\t", " ").replace("\n", " ")
        lines.append(f"{front}\t{back}")

    return "\n".join(lines)


def export_quiz_json(doc_id: str, db: Database) -> str:
    """Export quiz questions as formatted JSON."""
    questions = db.get_quiz_questions(doc_id)
    if not questions:
        return "[]"

    export_data = []
    for q in questions:
        export_data.append({
            "question": q["question"],
            "options": q.get("options", []),
            "correct": q.get("correct_answer_index", 0),
            "explanation": q.get("explanation", ""),
            "difficulty": q.get("difficulty", "medium"),
        })

    return json.dumps(export_data, indent=2, ensure_ascii=False)


def export_full_json(doc_id: str, db: Database) -> str:
    """Export complete document data as JSON."""
    data = db.get_full_document_data(doc_id)
    if not data:
        return "{}"

    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


def export_all_documents_csv(db: Database) -> str:
    """Export document list as CSV."""
    docs = db.list_documents()
    if not docs:
        return ""

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Filename", "Title", "Pages", "Size", "Status", "Created"])

    for doc in docs:
        writer.writerow([
            doc["id"],
            doc["filename"],
            doc.get("title", ""),
            doc.get("page_count", ""),
            doc.get("file_size", ""),
            doc.get("status", ""),
            doc.get("created_at", ""),
        ])

    return output.getvalue()


def save_export(content: str, default_name: str, parent_dir: Path | None = None) -> str | None:
    """Save exported content to a file. Returns path or None."""
    from PySide6.QtWidgets import QFileDialog

    directory = str(parent_dir or Path.home() / "Documents")
    file_path, _ = QFileDialog.getSaveFileName(
        None,
        "Export",
        f"{directory}/{default_name}",
        "All Files (*)",
    )

    if file_path:
        Path(file_path).write_text(content, encoding="utf-8")
        return file_path

    return None
