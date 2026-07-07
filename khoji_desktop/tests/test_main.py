from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest


class TestMain:
    def test_version(self):
        from khoji import __version__
        assert __version__ == "0.1.0"

    def test_main_imports(self):
        from khoji.main import main
        assert callable(main)

    def test_module_imports(self):
        import khoji.database.db
        import khoji.ai.embeddings
        import khoji.ai.llm
        import khoji.ai.vector_search
        import khoji.pipeline.content_generator
        import khoji.pipeline.exporter
        import khoji.pipeline.markdown_generator
        import khoji.pipeline.ocr
        import khoji.pipeline.pdf_extractor
        import khoji.pipeline.processor
        import khoji.ui.theme
        assert True

    def test_package_imports(self):
        import khoji
        import khoji.database
        import khoji.ai
        import khoji.pipeline
        import khoji.ui
        import khoji.utils
        assert True


class TestModuleExports:
    def test_database_exports(self):
        from khoji.database.db import Database, _connect, _now, _uuid
        assert callable(_connect)
        assert callable(_now)
        assert callable(_uuid)

    def test_embeddings_exports(self):
        from khoji.ai.embeddings import Embedder, get_embedder, EMBEDDING_DIM, MODEL_NAME
        assert EMBEDDING_DIM == 384

    def test_llm_exports(self):
        from khoji.ai.llm import LocalLLM, LLMConfig, get_llm, MODEL_PRESETS
        assert len(MODEL_PRESETS) >= 3

    def test_content_generator_exports(self):
        from khoji.pipeline.content_generator import Flashcard, QuizQuestion, generate_flashcards, generate_quiz
        assert callable(generate_flashcards)

    def test_pdf_extractor_exports(self):
        from khoji.pipeline.pdf_extractor import extract_pdf, ExtractionResult, ExtractedPage
        assert callable(extract_pdf)
