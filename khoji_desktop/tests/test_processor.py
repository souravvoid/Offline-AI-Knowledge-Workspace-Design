from __future__ import annotations

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from khoji.pipeline.processor import (
    ProcessingWorker,
    ProcessingResult,
    process_document_sync,
)


class TestProcessingWorker:
    def test_file_not_found(self, tmp_db):
        worker = ProcessingWorker("/nonexistent/file.pdf", tmp_db, extract_embeddings=False)
        result = worker.run()
        assert result.success is False
        assert "not found" in result.message

    def test_already_processed(self, tmp_db, tmp_path):
        file_path = tmp_path / "dup.pdf"
        file_path.write_text("fake content")
        doc = tmp_db.create_document(
            filename="dup.pdf",
            file_path=str(file_path),
            file_size=100,
        )
        worker = ProcessingWorker(str(file_path), tmp_db, extract_embeddings=False)
        result = worker.run()
        assert result.success is True
        assert "already processed" in result.message

    def test_processing_pipeline(self, sample_pdf_path, tmp_db):
        worker = ProcessingWorker(str(sample_pdf_path), tmp_db, extract_embeddings=False)
        result = worker.run()
        assert result.success is True
        assert result.doc_id != ""

    def test_ocr_fallback_on_empty_extraction(self, tmp_db):
        import tempfile
        import fitz
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            doc = fitz.open()
            doc.new_page()
            doc.save(f.name)
            doc.close()
            pdf_path = f.name
        worker = ProcessingWorker(pdf_path, tmp_db, extract_embeddings=False)
        result = worker.run()
        assert result.success is False
        Path(pdf_path).unlink(missing_ok=True)

    def test_progress_signal_emitted(self, sample_pdf_path, tmp_db):
        worker = ProcessingWorker(str(sample_pdf_path), tmp_db, extract_embeddings=False)
        progress_msgs = []
        worker.progress.connect(progress_msgs.append)
        result = worker.run()
        assert len(progress_msgs) > 0

    def test_processing_result_dataclass(self, sample_pdf_path, tmp_db):
        worker = ProcessingWorker(str(sample_pdf_path), tmp_db, extract_embeddings=False)
        result = worker.run()
        assert isinstance(result, ProcessingResult)
        assert isinstance(result.doc_id, str)
        assert isinstance(result.success, bool)


class TestProcessDocumentSync:
    def test_sync_processing(self, sample_pdf_path, tmp_db):
        result = process_document_sync(str(sample_pdf_path), tmp_db)
        assert isinstance(result, ProcessingResult)
