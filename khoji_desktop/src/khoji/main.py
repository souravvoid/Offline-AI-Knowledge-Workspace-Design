"""Khoji Desktop — main entry point.

Initializes database, creates the main window, registers all panels.
"""

from __future__ import annotations

import logging
import sys

from PySide6.QtWidgets import QApplication

from khoji.database.db import Database
from khoji.ui.main_window import MainWindow
from khoji.ui.panels.chat_panel import ChatView
from khoji.ui.panels.flashcards_panel import FlashcardsView
from khoji.ui.panels.library_panel import LibraryView
from khoji.ui.panels.notes_panel import NotesView
from khoji.ui.panels.quiz_panel import QuizView
from khoji.ui.panels.search_panel import SearchView

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("khoji")


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Khoji")
    app.setOrganizationName("Khoji")
    app.setStyle("Fusion")

    db = Database()
    logger.info("Database initialized at %s", db.db_path)

    window = MainWindow(db)

    # Create panels
    library = LibraryView(db)
    notes = NotesView(db)
    flashcards = FlashcardsView(db)
    quiz = QuizView(db)
    chat = ChatView(db)
    search = SearchView(db)

    # Register panels
    window.register_panel("library", library)
    window.register_panel("notes", notes)
    window.register_panel("flashcards", flashcards)
    window.register_panel("quiz", quiz)
    window.register_panel("chat", chat)
    window.register_panel("search", search)

    # Connect cross-panel signals
    def on_doc_selected(doc_id: str) -> None:
        notes.load_document(doc_id)
        flashcards.load_document(doc_id)
        quiz.load_document(doc_id)
        chat.load_document(doc_id)
        window.show_status("Document loaded")

    library.document_selected.connect(on_doc_selected)

    # Show
    window.show()
    logger.info("Khoji window shown")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
