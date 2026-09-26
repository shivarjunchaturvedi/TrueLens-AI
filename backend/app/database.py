"""
Database engine/session setup.

Uses SQLite by default via DATABASE_URL in .env. To move to PostgreSQL later,
change DATABASE_URL to e.g. postgresql+psycopg2://user:pass@host/dbname and
install psycopg2-binary — no other code changes are required because all
queries go through the SQLAlchemy ORM, not raw SQL.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Called once on application startup."""
    from app.models import user, scan  # noqa: F401  (ensure models are registered)
    Base.metadata.create_all(bind=engine)
