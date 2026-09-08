import sqlite3
from pathlib import Path

from backend.config import DATABASE_PATH
from backend.models import Conversation, Role, StoredMessage

SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL DEFAULT 'Nueva conversación',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role            TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content         TEXT NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
"""


class StorageError(Exception):
    """Error de la capa de almacenamiento."""


class ConversationNotFoundError(StorageError):
    """La conversación solicitada no existe."""


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 3000")
    return conn


def init_db(db_path: str) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = connect(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def create_conversation(db_path: str, title: str = "Nueva conversación") -> Conversation:
    conn = connect(db_path)
    try:
        cur = conn.execute("INSERT INTO conversations (title) VALUES (?)", (title,))
        conn.commit()
        row = conn.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
            (cur.lastrowid,),
        ).fetchone()
        return Conversation(**dict(row))
    except sqlite3.Error as exc:
        raise StorageError(f"Error de base de datos: {exc}") from exc
    finally:
        conn.close()


def list_conversations(db_path: str) -> list[Conversation]:
    conn = connect(db_path)
    try:
        rows = conn.execute(
            "SELECT id, title, created_at, updated_at FROM conversations ORDER BY updated_at DESC"
        ).fetchall()
        return [Conversation(**dict(row)) for row in rows]
    except sqlite3.Error as exc:
        raise StorageError(f"Error de base de datos: {exc}") from exc
    finally:
        conn.close()


def get_conversation(db_path: str, conversation_id: int) -> Conversation | None:
    conn = connect(db_path)
    try:
        row = conn.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()
        if row is None:
            return None
        return Conversation(**dict(row))
    except sqlite3.Error as exc:
        raise StorageError(f"Error de base de datos: {exc}") from exc
    finally:
        conn.close()


def add_message(
    db_path: str, conversation_id: int, role: Role, content: str
) -> StoredMessage:
    conn = connect(db_path)
    try:
        exists = conn.execute(
            "SELECT 1 FROM conversations WHERE id = ?", (conversation_id,)
        ).fetchone()
        if not exists:
            raise ConversationNotFoundError(
                f"No existe la conversación con id {conversation_id}"
            )
        cur = conn.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conversation_id, role, content),
        )
        conn.execute(
            "UPDATE conversations SET updated_at = datetime('now') WHERE id = ?",
            (conversation_id,),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, conversation_id, role, content, created_at FROM messages WHERE id = ?",
            (cur.lastrowid,),
        ).fetchone()
        return StoredMessage(**dict(row))
    except StorageError:
        raise
    except sqlite3.Error as exc:
        raise StorageError(f"Error de base de datos: {exc}") from exc
    finally:
        conn.close()


def list_messages(db_path: str, conversation_id: int) -> list[StoredMessage]:
    conn = connect(db_path)
    try:
        rows = conn.execute(
            "SELECT id, conversation_id, role, content, created_at FROM messages "
            "WHERE conversation_id = ? ORDER BY id ASC",
            (conversation_id,),
        ).fetchall()
        return [StoredMessage(**dict(row)) for row in rows]
    except sqlite3.Error as exc:
        raise StorageError(f"Error de base de datos: {exc}") from exc
    finally:
        conn.close()


def delete_message(db_path: str, message_id: int) -> None:
    conn = connect(db_path)
    try:
        conn.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()
    except sqlite3.Error as exc:
        raise StorageError(f"Error de base de datos: {exc}") from exc
    finally:
        conn.close()