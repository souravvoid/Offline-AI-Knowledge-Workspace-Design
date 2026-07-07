from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from khoji.database.db import Database


@pytest.fixture
def tmp_db() -> Database:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        db = Database(db_path)
        yield db
        db.close()


@pytest.fixture
def sample_text() -> str:
    return (
        "Python is a high-level programming language. "
        "It is widely used for web development and data science. "
        "The language emphasizes code readability. "
        "Functions are first-class objects in Python. "
        "A decorator is a function that takes another function and extends its behavior. "
        "Python supports multiple programming paradigms including object-oriented and functional programming. "
        "The Python interpreter has 14 standard data types. "
        "Exception handling in Python uses try-except blocks. "
        "List comprehensions provide a concise way to create lists. "
        "Modules help organize Python code into reusable files."
    )


@pytest.fixture
def sample_pdf_path() -> Path:
    import fitz
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 100), "This is a test PDF document.", fontsize=12)
        page.insert_text((50, 130), "It contains multiple lines of text.", fontsize=12)
        page.insert_text((50, 160), "Machine learning is transforming industries.", fontsize=12)
        doc.save(f.name)
        doc.close()
        return Path(f.name)
