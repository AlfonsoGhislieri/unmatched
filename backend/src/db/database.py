import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment (default to 'dev' if not set)
environment = os.getenv('ENV', 'dev')

# Select the database URL based on the environment
if environment == 'prod':
    DATABASE_URL = os.getenv('PROD_DATABASE_URL')
else:
    DATABASE_URL = os.getenv('DEV_DATABASE_URL')

# Create an engine
engine = create_engine(DATABASE_URL)

# Example usage: connect to the database
with engine.connect() as connection:
    result = connection.execute(text("SELECT 'Hello, world!'"))
    for row in result:
        print(row[0])