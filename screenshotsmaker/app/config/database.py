from threading import Lock

import sqlalchemy
from sqlalchemy.orm import Session

from app.config import settings

__engine: sqlalchemy.engine.base.Engine | None = None
__init_lock = Lock()


def initialize_database():
    """Initialize the SQLAlchemy database engine"""
    global __engine, __init_lock
    if __engine is not None:
        return
    with __init_lock:
        if __engine is not None:
            return

        connection_url = sqlalchemy.engine.url.URL.create(
            drivername=settings.DATABASE_DRIVER,
            username=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT,
            database=settings.DATABASE_NAME
        )

        kwargs = {}
        if settings.DATABASE_MAX_OVERFLOW is not None:
            kwargs["max_overflow"] = settings.DATABASE_MAX_OVERFLOW
        __engine = sqlalchemy.create_engine(
            url=connection_url,
            echo=settings.DATABASE_ECHO,
            pool_size=settings.DATABASE_POOL_SIZE,
            pool_pre_ping=True,
            pool_recycle=60,
            **kwargs
        )


def get_engine() -> sqlalchemy.engine.base.Engine:
    """Get the SQLAlchemy database engine"""
    global __engine
    if __engine is None:
        initialize_database()
    return __engine


def new_session() -> Session:
    """Create a new session"""
    return Session(get_engine())
