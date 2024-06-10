import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


# Handles the creation of the database engine and session factory.
def get_session_engine():
    load_dotenv()

    # Get the environment (default to 'dev' if not set)
    environment = os.getenv("ENV", "dev")

    if environment == "prod":
        DATABASE_URL = os.getenv("PROD_DATABASE_URL")
    else:
        DATABASE_URL = os.getenv("DEV_DATABASE_URL")

    engine = create_engine(
        DATABASE_URL
    )  # if you want to see log of actions add echo=True
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    return SessionLocal, engine
