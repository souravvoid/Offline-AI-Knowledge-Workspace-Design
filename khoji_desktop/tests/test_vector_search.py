from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import faiss
import numpy as np
import pytest

from khoji.ai.vector_search import VectorStore, get_vector_store, EMBEDDING_DIM


class TestVectorStoreInit:
    def test_default_path(self):
        store = VectorStore()
        assert store.store_path == Path.home() / ".khoji" / "vectors"
        assert store.store_path.exists()
        if store._index is not None:
            store._index.reset()

    def test_custom_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "vectors"
            store = VectorStore(path)
            assert store.store_path == path
            if store._index is not None:
                store._index.reset()


class TestAddVectors:
    def test_add_vectors(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = VectorStore(Path(tmp) / "v")
            store.add_vectors(
                chunk_ids=["c1", "c2"],
                embeddings=[[0.1] * EMBEDDING_DIM, [0.2] * EMBEDDING_DIM],
                metadata=[{"doc": "d1"}, {"doc": "d2"}],
            )
            assert store._index.ntotal == 2

    def test_add_empty_vectors(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = VectorStore(Path(tmp) / "v")
            store.add_vectors([], [])
            assert store._index.ntotal == 0


class TestSearch:
    def test_search_no_vectors(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = VectorStore(Path(tmp) / "v")
            assert store.search("test") == []

    def test_search_with_vectors(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = VectorStore(Path(tmp) / "v")
            store.add_vectors(
                chunk_ids=["c1"],
                embeddings=[[0.1] * EMBEDDING_DIM],
                metadata=[{"document_id": "d1"}],
            )
            with patch.object(store, "_index") as mock_index:
                mock_index.ntotal = 1
                mock_index.search.return_value = (
                    np.array([[0.5]], dtype=np.float32),
                    np.array([[0]], dtype=np.int64),
                )
                results = store.search("query", limit=5)
                assert len(results) > 0
                assert "chunk_id" in results[0]


class TestRemoveDocument:
    def test_remove_nonexistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = VectorStore(Path(tmp) / "v")
            assert store.remove_document("missing") == 0

    def test_remove_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = VectorStore(Path(tmp) / "v")
            store.add_vectors(
                chunk_ids=["c1", "c2"],
                embeddings=[[0.1] * EMBEDDING_DIM, [0.2] * EMBEDDING_DIM],
                metadata=[{"document_id": "d1"}, {"document_id": "d1"}],
            )
            removed = store.remove_document("d1")
            assert removed == 2
            assert store._index.ntotal == 0


class TestGetStats:
    def test_stats_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = VectorStore(Path(tmp) / "v")
            stats = store.get_stats()
            assert stats["total_vectors"] == 0
            assert stats["dimension"] == EMBEDDING_DIM


class TestGetVectorStore:
    def test_singleton(self):
        vs1 = get_vector_store()
        vs2 = get_vector_store()
        assert vs1 is vs2
