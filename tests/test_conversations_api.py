import logging

import pytest
from fastapi.testclient import TestClient

from backend.api import app, get_db_path
from backend.ollama_client import (
    OllamaConnectionError,
    OllamaHTTPError,
    OllamaModelError,
    OllamaTimeoutError,
)
from backend.storage import StorageError, init_db, list_messages


@pytest.fixture()
def api_client(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    app.dependency_overrides[get_db_path] = lambda: db
    with TestClient(app) as client:
        yield client, db
    app.dependency_overrides.clear()


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


def test_post_conversation_returns_201_with_default_title(api_client):
    client, _ = api_client

    response = client.post("/api/conversations", json={})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] >= 1
    assert body["title"] == "Nueva conversación"
    assert body["created_at"]
    assert body["updated_at"]


def test_post_conversation_with_custom_title(api_client):
    client, _ = api_client

    response = client.post("/api/conversations", json={"title": "Planificación"})

    assert response.status_code == 201
    assert response.json()["title"] == "Planificación"


def test_get_conversations_includes_created(api_client):
    client, _ = api_client
    client.post("/api/conversations", json={"title": "A"})
    client.post("/api/conversations", json={"title": "B"})

    response = client.get("/api/conversations")

    assert response.status_code == 200
    titles = [c["title"] for c in response.json()]
    assert "A" in titles
    assert "B" in titles


def test_get_conversation_returns_200(api_client):
    client, _ = api_client
    created = client.post("/api/conversations", json={"title": "X"}).json()

    response = client.get(f"/api/conversations/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_conversation_unknown_returns_404(api_client):
    client, _ = api_client

    response = client.get("/api/conversations/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "La conversación no existe."


def test_get_messages_empty_conversation_returns_empty_list(api_client):
    client, _ = api_client
    conv = client.post("/api/conversations", json={}).json()

    response = client.get(f"/api/conversations/{conv['id']}/messages")

    assert response.status_code == 200
    assert response.json() == []


def test_get_messages_unknown_conversation_returns_404(api_client):
    client, _ = api_client

    response = client.get("/api/conversations/999/messages")

    assert response.status_code == 404


def test_post_message_happy_path(api_client, monkeypatch):
    client, db = api_client
    conv = client.post("/api/conversations", json={}).json()
    fake = _patch_client(monkeypatch, reply="Hola, ¿en qué te ayudo?")

    response = client.post(
        f"/api/conversations/{conv['id']}/messages", json={"content": "Hola"}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["role"] == "assistant"
    assert body["content"] == "Hola, ¿en qué te ayudo?"
    assert body["conversation_id"] == conv["id"]
    assert fake.closed

    messages = list_messages(db, conv["id"])
    assert [m.role for m in messages] == ["user", "assistant"]
    assert messages[0].content == "Hola"
    assert messages[1].content == "Hola, ¿en qué te ayudo?"


def test_post_message_empty_content_returns_422(api_client):
    client, _ = api_client
    conv = client.post("/api/conversations", json={}).json()

    response = client.post(
        f"/api/conversations/{conv['id']}/messages", json={"content": ""}
    )

    assert response.status_code == 422


def test_post_message_unknown_conversation_does_not_insert(api_client):
    client, db = api_client

    response = client.post(
        "/api/conversations/999/messages", json={"content": "hola"}
    )

    assert response.status_code == 404
    assert list_messages(db, 999) == []


@pytest.mark.parametrize(
    "error,status_code",
    [
        (OllamaConnectionError("conn"), 503),
        (OllamaModelError("model"), 404),
        (OllamaTimeoutError("timeout"), 504),
        (OllamaHTTPError("http"), 502),
    ],
)
def test_ollama_error_is_mapped_and_user_message_removed(
    api_client, monkeypatch, error, status_code
):
    client, db = api_client
    conv = client.post("/api/conversations", json={}).json()
    _patch_client(monkeypatch, error=error)

    response = client.post(
        f"/api/conversations/{conv['id']}/messages", json={"content": "hola"}
    )

    assert response.status_code == status_code
    assert "detail" in response.json()
    assert list_messages(db, conv["id"]) == []


def test_retry_after_failure_does_not_duplicate_messages(api_client, monkeypatch):
    client, db = api_client
    conv = client.post("/api/conversations", json={}).json()
    _patch_client(monkeypatch, error=OllamaConnectionError("conn"))

    first = client.post(
        f"/api/conversations/{conv['id']}/messages", json={"content": "hola"}
    )

    assert first.status_code == 503
    assert list_messages(db, conv["id"]) == []

    _patch_client(monkeypatch, reply="respuesta")

    second = client.post(
        f"/api/conversations/{conv['id']}/messages", json={"content": "hola"}
    )

    assert second.status_code == 201
    assert [m.role for m in list_messages(db, conv["id"])] == ["user", "assistant"]


def test_rollback_failure_is_logged(api_client, monkeypatch, caplog):
    client, _ = api_client
    conv = client.post("/api/conversations", json={}).json()
    _patch_client(monkeypatch, error=OllamaConnectionError("conn"))

    def boom(db_path, message_id):
        raise StorageError("boom")

    monkeypatch.setattr("backend.api.delete_message", boom)

    with caplog.at_level(logging.ERROR, logger="backend.api"):
        response = client.post(
            f"/api/conversations/{conv['id']}/messages", json={"content": "hola"}
        )

    assert response.status_code == 503
    assert any("No se pudo eliminar" in record.message for record in caplog.records)


def test_storage_error_returns_500_generic(api_client, monkeypatch):
    client, _ = api_client

    def boom(db_path, title="Nueva conversación"):
        raise StorageError("boom")

    monkeypatch.setattr("backend.api.create_conversation", boom)

    response = client.post("/api/conversations", json={})

    assert response.status_code == 500
    assert response.json()["detail"] == "Error de almacenamiento."