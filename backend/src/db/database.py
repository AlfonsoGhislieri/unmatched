import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
    session_local = sessionmaker(bind=engine, autoflush=True, autocommit=False)

    return session_local, engine
