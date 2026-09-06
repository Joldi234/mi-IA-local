import httpx
import pytest
from backend.ollama_client import (
    OllamaClient,
    OllamaConnectionError,
    OllamaModelError,
    OllamaTimeoutError,
    OllamaHTTPError,
)

BASE_URL = "http://test.ollama"
MODEL = "qwen3:8b"
MESSAGES = [{"role": "user", "content": "Hola"}]


def _make_transport(handler):
    return httpx.MockTransport(handler)


def test_successful_response():
    def handler(request):
        assert request.url.path == "/api/chat"
        body = request.content
        assert b'"model"' in body
        assert b"qwen3:8b" in body
        assert b'"stream":false' in body
        return httpx.Response(
            200,
            json={
                "message": {
                    "role": "assistant",
                    "content": "Hola, soy Qwen3.",
                }
            },
        )

    client = OllamaClient(
        base_url=BASE_URL,
        model=MODEL,
        timeout=10,
    )
    client._client = httpx.Client(transport=_make_transport(handler), base_url=BASE_URL)

    result = client.send_messages(MESSAGES)
    assert result == "Hola, soy Qwen3."


def test_connection_refused():
    def handler(request):
        raise httpx.ConnectError("Connection refused")

    client = OllamaClient(base_url=BASE_URL, model=MODEL, timeout=10)
    client._client = httpx.Client(transport=_make_transport(handler), base_url=BASE_URL)

    with pytest.raises(OllamaConnectionError):
        client.send_messages(MESSAGES)


def test_model_not_found():
    def handler(request):
        return httpx.Response(404, text="model 'nope' not found")

    client = OllamaClient(base_url=BASE_URL, model=MODEL, timeout=10)
    client._client = httpx.Client(transport=_make_transport(handler), base_url=BASE_URL)

    with pytest.raises(OllamaModelError, match="no encontrado"):
        client.send_messages(MESSAGES)


def test_timeout():
    def handler(request):
        raise httpx.TimeoutException("timed out")

    client = OllamaClient(base_url=BASE_URL, model=MODEL, timeout=10)
    client._client = httpx.Client(transport=_make_transport(handler), base_url=BASE_URL)

    with pytest.raises(OllamaTimeoutError):
        client.send_messages(MESSAGES)


def test_http_error():
    def handler(request):
        return httpx.Response(500, text="Internal Server Error")

    client = OllamaClient(base_url=BASE_URL, model=MODEL, timeout=10)
    client._client = httpx.Client(transport=_make_transport(handler), base_url=BASE_URL)

    with pytest.raises(OllamaHTTPError, match="500"):
        client.send_messages(MESSAGES)


def test_404_not_model_related():
    def handler(request):
        return httpx.Response(404, text="route not found")

    client = OllamaClient(base_url=BASE_URL, model=MODEL, timeout=10)
    client._client = httpx.Client(transport=_make_transport(handler), base_url=BASE_URL)

    with pytest.raises(OllamaHTTPError, match="404"):
        client.send_messages(MESSAGES)
