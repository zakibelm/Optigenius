import os
from types import SimpleNamespace
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.app.db import Base
from backend.app import repo


def _engine_or_xfail():
    url = os.getenv("DATABASE_URL")
    if not url or not url.startswith("postgresql"):
        pytest.xfail(
            "Postgres non dispo. Définis DATABASE_URL et lance Postgres.\n"
            "Astuce (Docker): docker run --name pg -e POSTGRES_PASSWORD=dev "
            "-e POSTGRES_DB=optigenius -p 5432:5432 -d postgres:16"
        )
    try:
        engine = create_engine(url, future=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        pytest.xfail(f"Connexion Postgres impossible: {e}")


def test_postgres_roundtrip():
    engine = _engine_or_xfail()
    Base.metadata.create_all(engine)  # au cas où la migration n'a pas été lancée
    Session = sessionmaker(bind=engine, future=True)
    with Session() as s:
        payload = SimpleNamespace(
            name="Bob", phone="000", datetime="2025-02-02T09:00:00Z", notes=None
        )
        row = repo.create_appointment(s, payload)
        assert row.id is not None
