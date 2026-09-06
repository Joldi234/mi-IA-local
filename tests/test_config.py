import os
import pytest
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT


class TestConfigDefaults:
    def test_base_url_default(self):
        assert OLLAMA_BASE_URL == "http://localhost:11434"

    def test_model_default(self):
        assert OLLAMA_MODEL == "qwen3:8b"

    def test_timeout_default(self):
        assert OLLAMA_TIMEOUT == 120


class TestConfigFromEnv:
    def test_env_overrides(self, monkeypatch):
        monkeypatch.setenv("OLLAMA_BASE_URL", "http://custom:9999")
        monkeypatch.setenv("OLLAMA_MODEL", "llama3")
        monkeypatch.setenv("OLLAMA_TIMEOUT", "30")

        import importlib
        import backend.config as config_mod
        importlib.reload(config_mod)

        assert config_mod.OLLAMA_BASE_URL == "http://custom:9999"
        assert config_mod.OLLAMA_MODEL == "llama3"
        assert config_mod.OLLAMA_TIMEOUT == 30

        importlib.reload(config_mod)
