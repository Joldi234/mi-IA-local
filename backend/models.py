from typing import Literal

from pydantic import BaseModel, Field

Role = Literal["user", "assistant"]


class Conversation(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str


class ConversationCreate(BaseModel):
    title: str = "Nueva conversación"


class StoredMessage(BaseModel):
    id: int
    conversation_id: int
    role: Role
    content: str
    created_at: str


class StoredMessageCreate(BaseModel):
    role: Role
    content: str = Field(min_length=1)


class MessageRequest(BaseModel):
    content: str = Field(min_length=1)