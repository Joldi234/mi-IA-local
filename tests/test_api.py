import pytest
from fastapi.testclient import TestClient

from backend.ollama_client import (
    OllamaConnectionError,
    OllamaHTTPError,
    OllamaModelError,
    OllamaTimeoutError,
)
from backend.api import app

client = TestClient(app)

MESSAGES = {"messages": [{"role": "user", "content": "Hola"}]}


class FakeOllamaClient:
    def __init__(self, reply="hola", error=None):
        self.reply = reply
        self.error = error
        self.closed = False

    def send_messages(self, messages):
        if self.error:
            raise self.error
        return self.reply

    def close(self):
        self.closed = True


def _patch_client(monkeypatch, **kwargs):
    fake = FakeOllamaClient(**kwargs)
    monkeypatch.setattr("backend.api.OllamaClient", lambda: fake)
    return fake


def test_valid_request_returns_reply(monkeypatch):
    fake = _patch_client(monkeypatch, reply="Hola, soy Qwen3.")
    response = client.post("/api/chat", json=MESSAGES)

    assert response.status_code == 200
    assert response.json() == {"reply": "Hola, soy Qwen3."}
    assert fake.closed


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"messages": []},
        {"messages": [{"role": "admin", "content": "Hola"}]},
    ],
)
def test_invalid_payload_returns_422(payload):
    response = client.post("/api/chat", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "error,status_code",
    [
        (OllamaConnectionError("conn"), 503),
        (OllamaModelError("model"), 404),
        (OllamaTimeoutError("timeout"), 504),
        (OllamaHTTPError("http"), 502),
    ],
)
def test_ollama_errors_are_translated(monkeypatch, error, status_code):
    fake = _patch_client(monkeypatch, error=error)
    response = client.post("/api/chat", json=MESSAGES)

    assert response.status_code == status_code
    assert "detail" in response.json()
    assert fake.closed