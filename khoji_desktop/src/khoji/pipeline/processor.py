"""Processing pipeline orchestrator.

Coordinates: PDF extraction → OCR → chunking → embeddings → markdown → flashcards → quiz.
Runs in a QThread to avoid blocking the UI.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from khoji.database.db import Database
from khoji.pipeline.content_generator import generate_flashcards, generate_quiz
from khoji.pipeline.markdown_generator import chunk_markdown, generate_markdown
from khoji.pipeline.ocr import has_ocr_engine, ocr_image
from khoji.pipeline.pdf_extractor import extract_pdf

logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    doc_id: str
    success: bool
    message: str = ""
    page_count: int = 0
    chunk_count: int = 0
    flashcard_count: int = 0
    quiz_count: int = 0


class ProcessingWorker(QThread):
    """Background worker for document processing."""

    progress = Signal(str)
    finished = Signal(object)

    def __init__(
        self,
        file_path: str,
        db: Database,
        *,
        extract_embeddings: bool = True,
    ) -> None:
        super().__init__()
        self.file_path = file_path
        self.db = db
        self.extract_embeddings = extract_embeddings

    def run(self) -> ProcessingResult:
        path = Path(self.file_path)

        if not path.exists():
            return ProcessingResult(doc_id="", success=False, message="File not found")

        existing = self.db.document_exists(str(path))
        if existing:
            return ProcessingResult(
                doc_id=existing["id"],
                success=True,
                message="Document already processed",
            )

        self.progress.emit("Creating document record...")
        doc = self.db.create_document(
            filename=path.name,
            file_path=str(path),
            file_size=path.stat().st_size,
        )
        doc_id = doc["id"]

        try:
            # Step 1: Extract text
            self.progress.emit("Extracting text from PDF...")
            extraction = extract_pdf(path)
            page_count = extraction.page_count

            if extraction.errors:
                logger.warning("Extraction warnings: %s", extraction.errors)

            if not extraction.full_text.strip():
                # Try OCR fallback
                if has_ocr_engine():
                    self.progress.emit("No text found. Running OCR...")
                    extraction = self._ocr_fallback(path, page_count)

            if not extraction.full_text.strip():
                self.db.update_document(doc_id, status="failed")
                return ProcessingResult(
                    doc_id=doc_id,
                    success=False,
                    message="No text could be extracted",
                )

            self.progress.emit(f"Extracted {len(extraction.full_text):,} characters from {page_count} pages")
            self.db.update_document(doc_id, page_count=page_count, status="processed")

            # Step 2: Generate markdown
            self.progress.emit("Generating markdown...")
            markdown = generate_markdown(
                filename=path.name,
                text=extraction.full_text,
                page_count=page_count,
            )
            self.db.upsert_notes(doc_id, markdown)

            # Step 3: Chunk text
            self.progress.emit("Chunking text for indexing...")
            chunks = chunk_markdown(extraction.full_text)
            self.db.add_chunks(doc_id, chunks)

            # Step 4: Embeddings (optional, deferred if slow)
            if self.extract_embeddings:
                self.progress.emit("Generating embeddings...")
                try:
                    from khoji.ai.embeddings import get_embedder
                    from khoji.ai.vector_search import get_vector_store

                    embedder = get_embedder()
                    store = get_vector_store()

                    chunk_texts = [c["content"] for c in chunks]
                    embeddings = embedder.embed(chunk_texts)

                    valid = [(i, e) for i, e in enumerate(embeddings) if e]
                    if valid:
                        ids = [f"{doc_id}_chunk_{i}" for i, _ in valid]
                        vecs = [e for _, e in valid]
                        metas = [{"document_id": doc_id, "chunk_index": chunks[i]["chunk_index"]} for i, _ in valid]
                        store.add_vectors(ids, vecs, metas)
                except Exception as e:
                    logger.warning("Embedding generation failed (non-fatal): %s", e)

            # Step 5: Flashcards
            self.progress.emit("Generating flashcards...")
            flashcards = generate_flashcards(extraction.full_text)
            self.db.add_flashcards(doc_id, [vars(c) for c in flashcards])

            # Step 6: Quiz questions
            self.progress.emit("Generating quiz questions...")
            quiz = generate_quiz(extraction.full_text)
            self.db.add_quiz_questions(doc_id, [vars(q) for q in quiz])

            self.progress.emit(f"Done! {len(flashcards)} flashcards, {len(quiz)} quiz questions")

            return ProcessingResult(
                doc_id=doc_id,
                success=True,
                message="Processed successfully",
                page_count=page_count,
                chunk_count=len(chunks),
                flashcard_count=len(flashcards),
                quiz_count=len(quiz),
            )

        except Exception as e:
            logger.error("Processing failed: %s", e)
            self.db.update_document(doc_id, status="failed")
            return ProcessingResult(doc_id=doc_id, success=False, message=str(e))

    def _ocr_fallback(self, path: Path, page_count: int):
        """Run OCR on pages that have no text."""
        from khoji.pipeline.pdf_extractor import ExtractionResult, ExtractedPage

        result = ExtractionResult(filename=path.name, page_count=page_count)
        all_text = []
        offset = 0

        try:
            import fitz

            doc = fitz.open(str(path))
            for i in range(min(page_count, 20)):
                self.progress.emit(f"OCR: page {i + 1}/{page_count}...")
                page = doc.load_page(i)
                pix = page.get_pixmap(dpi=150)
                img_path = path.parent / f"_ocr_tmp_{i}.png"
                pix.save(str(img_path))

                ocr_result = ocr_image(img_path)
                try:
                    img_path.unlink()
                except OSError:
                    pass

                if ocr_result.text.strip():
                    result.pages.append(
                        ExtractedPage(
                            page_number=i + 1,
                            text=ocr_result.text,
                            char_offset=offset,
                            char_length=len(ocr_result.text),
                        )
                    )
                    all_text.append(ocr_result.text)
                    offset += len(ocr_result.text)

            doc.close()
        except Exception as e:
            logger.error("OCR fallback failed: %s", e)

        result.full_text = "\n\n".join(all_text)
        return result


def process_document_sync(file_path: str, db: Database) -> ProcessingResult:
    """Synchronous processing for CLI/test usage."""
    worker = ProcessingWorker(file_path, db, extract_embeddings=False)
    return worker.run()
