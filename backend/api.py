import logging

from contextlib import asynccontextmanager

from typing import Literal

from fastapi import Depends
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.config import DATABASE_PATH
from backend.models import Conversation, ConversationCreate, MessageRequest, StoredMessage
from backend.ollama_client import (
    OllamaClient,
    OllamaConnectionError,
    OllamaHTTPError,
    OllamaModelError,
    OllamaTimeoutError,
)
from backend.storage import (
    StorageError,
    add_message,
    create_conversation,
    delete_message,
    get_conversation,
    init_db,
    list_conversations,
    list_messages,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa la base SQLite al arrancar para que una instalación limpia
    # funcione sin ejecutar init_db() manualmente. Usa la misma ruta que los
    # endpoints (get_db_path), por lo que en tests respeta dependency_overrides.
    resolve_db_path = app.dependency_overrides.get(get_db_path, get_db_path)
    init_db(resolve_db_path())
    yield

app = FastAPI(title="mi-IA-local API", lifespan=lifespan)
logger = logging.getLogger("backend.api")


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


def get_db_path() -> str:
    return DATABASE_PATH


def _map_ollama_error(exc: Exception) -> HTTPException:
    if isinstance(exc, OllamaConnectionError):
        return HTTPException(
            status_code=503,
            detail="No se pudo conectar con Ollama. Verifique que esté ejecutándose.",
        )
    if isinstance(exc, OllamaModelError):
        return HTTPException(
            status_code=404,
            detail="El modelo configurado no existe en Ollama.",
        )
    if isinstance(exc, OllamaTimeoutError):
        return HTTPException(
            status_code=504,
            detail="La conexión con Ollama expiró. El modelo puede estar cargando.",
        )
    if isinstance(exc, OllamaHTTPError):
        return HTTPException(
            status_code=502,
            detail="Ollama devolvió un error al procesar la solicitud.",
        )
    return HTTPException(status_code=500, detail="Error de almacenamiento.")


@app.post("/api/conversations", response_model=Conversation, status_code=201)
def post_conversation(request: ConversationCreate, db_path: str = Depends(get_db_path)):
    try:
        return create_conversation(db_path, title=request.title)
    except StorageError:
        raise HTTPException(status_code=500, detail="Error de almacenamiento.")


@app.get("/api/conversations", response_model=list[Conversation])
def get_conversations(db_path: str = Depends(get_db_path)):
    try:
        return list_conversations(db_path)
    except StorageError:
        raise HTTPException(status_code=500, detail="Error de almacenamiento.")


@app.get("/api/conversations/{conversation_id}", response_model=Conversation)
def get_conversation_by_id(conversation_id: int, db_path: str = Depends(get_db_path)):
    try:
        conversation = get_conversation(db_path, conversation_id)
    except StorageError:
        raise HTTPException(status_code=500, detail="Error de almacenamiento.")
    if conversation is None:
        raise HTTPException(status_code=404, detail="La conversación no existe.")
    return conversation


@app.get(
    "/api/conversations/{conversation_id}/messages",
    response_model=list[StoredMessage],
)
def get_conversation_messages(
    conversation_id: int, db_path: str = Depends(get_db_path)
):
    try:
        conversation = get_conversation(db_path, conversation_id)
    except StorageError:
        raise HTTPException(status_code=500, detail="Error de almacenamiento.")
    if conversation is None:
        raise HTTPException(status_code=404, detail="La conversación no existe.")
    try:
        return list_messages(db_path, conversation_id)
    except StorageError:
        raise HTTPException(status_code=500, detail="Error de almacenamiento.")


@app.post(
    "/api/conversations/{conversation_id}/messages",
    response_model=StoredMessage,
    status_code=201,
)
def post_conversation_message(
    conversation_id: int,
    request: MessageRequest,
    db_path: str = Depends(get_db_path),
):
    try:
        conversation = get_conversation(db_path, conversation_id)
    except StorageError:
        raise HTTPException(status_code=500, detail="Error de almacenamiento.")
    if conversation is None:
        raise HTTPException(status_code=404, detail="La conversación no existe.")

    try:
        user_msg = add_message(db_path, conversation_id, "user", request.content)
        history = list_messages(db_path, conversation_id)
    except StorageError:
        raise HTTPException(status_code=500, detail="Error de almacenamiento.")

    payload = [{"role": m.role, "content": m.content} for m in history]

    client = OllamaClient()
    try:
        reply = client.send_messages(payload)
    except (
        OllamaConnectionError,
        OllamaModelError,
        OllamaTimeoutError,
        OllamaHTTPError,
    ) as exc:
        try:
            delete_message(db_path, user_msg.id)
        except Exception as err:
            logger.error(
                "No se pudo eliminar el mensaje del usuario tras el fallo de Ollama: %s",
                err,
            )
        raise _map_ollama_error(exc)
    finally:
        client.close()

    try:
        assistant_msg = add_message(db_path, conversation_id, "assistant", reply)
    except StorageError:
        raise HTTPException(status_code=500, detail="Error de almacenamiento.")
    return assistant_msg