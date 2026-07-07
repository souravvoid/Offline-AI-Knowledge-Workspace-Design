from __future__ import annotations

from unittest.mock import patch

import pytest

from khoji.ai.embeddings import Embedder, get_embedder, EMBEDDING_DIM


class TestEmbedderInit:
    def test_initial_state(self):
        e = Embedder()
        assert e.state.loaded is False
        assert e._model is None
        assert e.is_loaded() is False


class TestEmbedderLoad:
    def test_load_failure_graceful(self):
        e = Embedder()
        with patch("sentence_transformers.SentenceTransformer", side_effect=ImportError):
            result = e.load()
            assert result is False
            assert "failed" in e.state.error.lower()

    def test_load_already_loaded(self):
        e = Embedder()
        e._model = True
        assert e.load() is True


class TestEmbed:
    def test_embed_failure_returns_empty(self):
        e = Embedder()
        e.state.loaded = True
        e._model = True
        with patch.object(e, "load", return_value=False):
            result = e.embed(["test"])
            assert result == [[]]


class TestEmbedOne:
    def test_embed_one_returns_list(self):
        e = Embedder()
        result = e.embed_one("test")
        assert isinstance(result, list)


class TestGetInfo:
    def test_get_info_defaults(self):
        e = Embedder()
        info = e.get_info()
        assert info["dimension"] == EMBEDDING_DIM
        assert info["loaded"] is False


class TestGetEmbedder:
    def test_singleton(self):
        e1 = get_embedder()
        e2 = get_embedder()
        assert e1 is e2
