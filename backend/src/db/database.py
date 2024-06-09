from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# TODO: pull this into a .env file and manage URLs for dev / prod
DATABASE_URL = "postgresql+psycopg2://devuser:devpassword@localhost:5432/devunmatched"

# Create an engine
engine = create_engine(DATABASE_URL)

# Example usage: connect to the database
with engine.connect() as connection:
    result = connection.execute(text("SELECT 'Hello, world!'"))
    for row in result:
        print(row[0])