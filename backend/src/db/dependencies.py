from db.database import get_session_engine

SessionLocal, _ = get_session_engine()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()