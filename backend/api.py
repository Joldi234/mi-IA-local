from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.ollama_client import (
    OllamaClient,
    OllamaConnectionError,
    OllamaHTTPError,
    OllamaModelError,
    OllamaTimeoutError,
)

app = FastAPI(title="mi-IA-local API")


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1)


class ChatResponse(BaseModel):
    reply: str


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    client = OllamaClient()
    try:
        reply = client.send_messages([m.model_dump() for m in request.messages])
    except OllamaConnectionError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con Ollama. Verifique que esté ejecutándose.",
        )
    except OllamaModelError:
        raise HTTPException(
            status_code=404,
            detail="El modelo configurado no existe en Ollama.",
        )
    except OllamaTimeoutError:
        raise HTTPException(
            status_code=504,
            detail="La conexión con Ollama expiró. El modelo puede estar cargando.",
        )
    except OllamaHTTPError:
        raise HTTPException(
            status_code=502,
            detail="Ollama devolvió un error al procesar la solicitud.",
        )
    finally:
        client.close()
    return ChatResponse(reply=reply)