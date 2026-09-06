import httpx
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT


class OllamaConnectionError(Exception):
    pass


class OllamaModelError(Exception):
    pass


class OllamaTimeoutError(Exception):
    pass


class OllamaHTTPError(Exception):
    pass


class OllamaClient:
    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL,
        timeout: int = OLLAMA_TIMEOUT,
    ):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def send_messages(self, messages: list[dict[str, str]]) -> str:
        payload = {"model": self.model, "messages": messages, "stream": False}
        try:
            response = self._client.post("/api/chat", json=payload)
        except httpx.ConnectError:
            raise OllamaConnectionError(
                "No se pudo conectar con Ollama. Verifique que este ejecutándose."
            )
        except httpx.TimeoutException:
            raise OllamaTimeoutError(
                "La conexión con Ollama expiró. El modelo puede estar cargando."
            )

        if response.status_code == 404:
            body = response.text.lower()
            if "model" in body and "not found" in body:
                raise OllamaModelError(
                    f"Modelo '{self.model}' no encontrado en Ollama."
                )
            raise OllamaHTTPError(
                f"Error HTTP 404: {response.text}"
            )

        if response.status_code >= 400:
            raise OllamaHTTPError(
                f"Error HTTP {response.status_code}: {response.text}"
            )

        data = response.json()
        return data["message"]["content"]

    def close(self):
        self._client.close()
