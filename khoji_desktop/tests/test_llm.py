from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from khoji.ai.llm import (
    LocalLLM,
    LLMConfig,
    LLMState,
    get_llm,
    MODEL_PRESETS,
)


class TestLLMConfig:
    def test_default_config(self):
        cfg = LLMConfig()
        assert cfg.model_name == "qwen2.5-0.5b"
        assert cfg.temperature == 0.7
        assert cfg.max_tokens == 2048


class TestLLMInit:
    def test_default_config(self):
        llm = LocalLLM()
        assert llm.state.loaded is False
        assert llm._llm is None

    def test_custom_config(self):
        cfg = LLMConfig(model_name="tinyllama-1.1b", temperature=0.5)
        llm = LocalLLM(cfg)
        assert llm.config.model_name == "tinyllama-1.1b"


class TestDetectHardware:
    def test_detect_returns_config(self):
        llm = LocalLLM()
        mock_psutil = MagicMock()
        mock_psutil.virtual_memory.return_value.available = 8 * 1024 * 1024 * 1024
        with patch.dict(sys.modules, {"psutil": mock_psutil}):
            cfg = llm.detect_hardware()
            assert isinstance(cfg, LLMConfig)

    def test_detect_no_psutil(self):
        llm = LocalLLM()
        if "psutil" in sys.modules:
            del sys.modules["psutil"]
        cfg = llm.detect_hardware()
        assert cfg.model_name in MODEL_PRESETS

    def test_regression_bug4_quality_comparison(self):
        """BUG-4: String comparison of quality ("high" > "medium") works but is fragile."""
        llm = LocalLLM()
        mock_psutil = MagicMock()
        mock_psutil.virtual_memory.return_value.available = 8 * 1024 * 1024 * 1024
        with patch.dict(sys.modules, {"psutil": mock_psutil}):
            cfg = llm.detect_hardware()
            assert cfg.model_name in MODEL_PRESETS
            preset = MODEL_PRESETS[cfg.model_name]
            assert preset["quality"] in ("high", "medium", "low")


class TestEnsureModel:
    def test_unknown_model(self):
        llm = LocalLLM(LLMConfig(model_name="unknown"))
        result = llm.ensure_model()
        assert result is False
        assert "Unknown" in llm.state.error

    def test_model_already_exists(self, tmp_path):
        llm = LocalLLM(LLMConfig(model_name="qwen2.5-0.5b"))
        with patch("khoji.ai.llm.GGUF_DIR", tmp_path):
            model_file = tmp_path / MODEL_PRESETS["qwen2.5-0.5b"]["filename"]
            model_file.parent.mkdir(parents=True, exist_ok=True)
            model_file.write_text("fake model")
            result = llm.ensure_model()
            assert result is True
            assert llm.state.model_path == str(model_file)


class TestLoad:
    def test_load_without_model_path_fails(self):
        llm = LocalLLM()
        with patch.object(llm, "ensure_model", return_value=False):
            result = llm.load()
            assert result is False

    def test_already_loaded(self):
        llm = LocalLLM()
        llm._llm = MagicMock()
        assert llm.load() is True


class TestGenerate:
    def test_generate_without_load(self):
        llm = LocalLLM()
        result = llm.generate("Hello")
        assert result.startswith("[Error:")


class TestGenerateStream:
    def test_stream_without_load(self):
        llm = LocalLLM()
        results = list(llm.generate_stream("Hello"))
        assert len(results) == 1
        assert results[0].startswith("[Error:")


class TestIsLoaded:
    def test_not_loaded(self):
        llm = LocalLLM()
        assert llm.is_loaded() is False


class TestUnload:
    def test_unload(self):
        llm = LocalLLM()
        llm._llm = MagicMock()
        llm.state.loaded = True
        llm.unload()
        assert llm._llm is None
        assert llm.state.loaded is False


class TestGetInfo:
    def test_default_info(self):
        llm = LocalLLM()
        info = llm.get_info()
        assert info["loaded"] is False
        assert info["error"] == ""


class TestGetLLM:
    def test_singleton(self):
        llm1 = get_llm()
        llm2 = get_llm()
        assert llm1 is llm2
