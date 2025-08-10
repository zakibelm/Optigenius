from types import SimpleNamespace
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from backend.app.db import Base
from backend.app import models, repo


def make_sqlite_session():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)


def test_create_appointment_ok():
    Session = make_sqlite_session()
    with Session() as s:
        payload = SimpleNamespace(
            name="Alice",
            phone="+33123456789",
            datetime="2025-01-01T10:00:00Z",
            notes="First",
        )
        obj = repo.create_appointment(s, payload)
        assert obj.id is not None
        assert obj.name == "Alice"
        assert obj.datetime.endswith("Z")
        assert obj.created_at is not None


def test_constraints_not_null():
    Session = make_sqlite_session()
    with Session() as s:
        bad = models.Appointment(  # type: ignore[arg-type]
            name=None, phone="x", datetime="2025-01-01T00:00:00Z"
        )
        s.add(bad)
        with pytest.raises(IntegrityError):
            s.commit()
