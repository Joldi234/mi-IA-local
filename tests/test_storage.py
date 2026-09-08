import sqlite3

import pytest
from pydantic import ValidationError

from backend.models import StoredMessageCreate
from backend.storage import (
    ConversationNotFoundError,
    add_message,
    connect,
    create_conversation,
    delete_message,
    get_conversation,
    init_db,
    list_conversations,
    list_messages,
)


def test_init_db_creates_tables_and_index(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)

    conn = connect(db)
    try:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
        indexes = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'index'"
            ).fetchall()
        }
    finally:
        conn.close()

    assert "conversations" in tables
    assert "messages" in tables
    assert "idx_messages_conversation" in indexes


def test_init_db_is_idempotent(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    init_db(db)


def test_create_conversation(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)

    conv = create_conversation(db)

    assert conv.id >= 1
    assert conv.title == "Nueva conversación"
    assert conv.created_at
    assert conv.updated_at


def test_list_conversations_orders_by_updated_at_desc(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    create_conversation(db, "B")
    create_conversation(db, "A")

    conn = connect(db)
    try:
        conn.execute(
            "UPDATE conversations SET updated_at = '2026-01-02 10:00:00' WHERE id = 1"
        )
        conn.execute(
            "UPDATE conversations SET updated_at = '2026-01-03 10:00:00' WHERE id = 2"
        )
        conn.commit()
    finally:
        conn.close()

    convs = list_conversations(db)

    assert [c.title for c in convs] == ["A", "B"]


def test_get_conversation_returns_conversation(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    created = create_conversation(db, "Test")

    conv = get_conversation(db, created.id)

    assert conv is not None
    assert conv.id == created.id
    assert conv.title == "Test"


def test_get_conversation_unknown_id_returns_none(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)

    assert get_conversation(db, 999) is None


def test_add_message_user_and_assistant_round_trip(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    conv = create_conversation(db)

    user_msg = add_message(db, conv.id, "user", "Hola")
    assistant_msg = add_message(db, conv.id, "assistant", "Hola, ¿en qué te ayudo?")

    assert user_msg.id >= 1
    assert user_msg.conversation_id == conv.id
    assert user_msg.role == "user"
    assert user_msg.content == "Hola"
    assert user_msg.created_at

    assert assistant_msg.id > user_msg.id
    assert assistant_msg.role == "assistant"
    assert assistant_msg.content == "Hola, ¿en qué te ayudo?"


def test_list_messages_returns_insertion_order(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    conv = create_conversation(db)
    for content in ["uno", "dos", "tres"]:
        add_message(db, conv.id, "user", content)

    msgs = list_messages(db, conv.id)

    assert [m.content for m in msgs] == ["uno", "dos", "tres"]
    assert [m.id for m in msgs] == sorted(m.id for m in msgs)


def test_role_validation_pydantic_rejects_invalid():
    with pytest.raises(ValidationError):
        StoredMessageCreate(role="admin", content="hola")


def test_sqlite_check_rejects_invalid_role(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    conv = create_conversation(db)

    conn = connect(db)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conv.id, "admin", "hola"),
            )
    finally:
        conn.close()


def test_add_message_unknown_conversation_raises_not_found(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)

    with pytest.raises(ConversationNotFoundError):
        add_message(db, 999, "user", "hola")


def test_fk_rejects_direct_insert_with_bad_conversation_id(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)

    conn = connect(db)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (999, "user", "hola"),
            )
    finally:
        conn.close()


def test_messages_cascade_when_conversation_deleted(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    conv = create_conversation(db)
    add_message(db, conv.id, "user", "hola")

    conn = connect(db)
    try:
        conn.execute("DELETE FROM conversations WHERE id = ?", (conv.id,))
        conn.commit()
    finally:
        conn.close()

    assert list_messages(db, conv.id) == []


def test_updated_at_refreshed_after_add_message(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    conv = create_conversation(db)
    add_message(db, conv.id, "user", "hola")

    updated = get_conversation(db, conv.id)

    assert updated is not None
    assert updated.updated_at
    assert updated.updated_at >= conv.updated_at


def test_persistence_across_connections(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    conv = create_conversation(db, "Persistente")
    add_message(db, conv.id, "user", "hola persistente")

    convs = list_conversations(db)
    msgs = list_messages(db, conv.id)

    assert convs[0].id == conv.id
    assert convs[0].title == "Persistente"
    assert msgs[0].content == "hola persistente"
    assert msgs[0].role == "user"


def test_delete_message_removes_only_selected_message(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    conv = create_conversation(db)
    first = add_message(db, conv.id, "user", "uno")
    second = add_message(db, conv.id, "assistant", "dos")

    delete_message(db, first.id)

    remaining = list_messages(db, conv.id)
    assert [m.id for m in remaining] == [second.id]
    assert remaining[0].content == "dos"


def test_delete_message_unknown_id_does_not_raise(tmp_path):
    db = str(tmp_path / "test.db")
    init_db(db)
    conv = create_conversation(db)
    add_message(db, conv.id, "user", "uno")

    delete_message(db, 999)
    delete_message(db, 999999)

    assert len(list_messages(db, conv.id)) == 1