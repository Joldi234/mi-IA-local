import sqlite3

from fastapi.testclient import TestClient

from backend.api import app


def test_lifespan_initializes_fresh_database(tmp_path, monkeypatch):
    """Una BD SQLite nueva queda inicializada al arrancar la app (lifespan),
    sin ejecutar init_db() manualmente."""
    db_file = tmp_path / "clean.db"
    monkeypatch.setattr("backend.api.DATABASE_PATH", str(db_file))

    with TestClient(app) as client:
        # El archivo de base de datos existe y puede utilizarse.
        assert db_file.exists()

        conn = sqlite3.connect(str(db_file))
        try:
            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
        finally:
            conn.close()
        assert {"conversations", "messages"} <= tables

        # Un endpoint de conversaciones funciona sobre la BD limpia.
        created = client.post("/api/conversations", json={})
        assert created.status_code == 201

        listed = client.get("/api/conversations")
        assert listed.status_code == 200
        assert len(listed.json()) == 1