from db.database import get_session_engine

session_local, _ = get_session_engine()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
