import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_database_connection():
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

    # Connect to the database
    connection = engine.connect()
    return connection
