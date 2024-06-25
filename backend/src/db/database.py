from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


# Handles the creation of the database engine and session factory.
def get_session_engine():
    engine = create_engine(settings.DATABASE_URL)
    session_local = sessionmaker(
        bind=engine, autoflush=True, autocommit=False
    )  # if you want to see log of actions add echo=True
    return session_local, engine


session_local, engine = get_session_engine()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
