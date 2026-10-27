import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


@lru_cache(maxsize=1)
def get_engine():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set before using the database.")
    return create_engine(database_url, pool_pre_ping=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()
