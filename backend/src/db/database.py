import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_database_connection():
    load_dotenv()

    # Get the environment (default to 'dev' if not set)
    environment = os.getenv('ENV', 'dev')

    if environment == 'prod':
        DATABASE_URL = os.getenv('PROD_DATABASE_URL')
    else:
        DATABASE_URL = os.getenv('DEV_DATABASE_URL')

    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    
    return connection
