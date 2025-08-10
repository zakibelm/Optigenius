import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# DATABASE_URL (postgresql+psycopg://user:pass@host:port/db)
# fallback SQLite in-memory pour tests unitaires
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+pysqlite:///:memory:?cache=shared")


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
