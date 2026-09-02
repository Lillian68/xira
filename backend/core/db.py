from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from config.config import Config


class Base(DeclarativeBase):
    pass


engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_reset_on_return="rollback",
)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    return SessionLocal()


def close_db():
    SessionLocal.remove()
    engine.dispose()


def init_db():
    import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
