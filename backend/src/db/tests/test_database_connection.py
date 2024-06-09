import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from db.database import get_database_connection

@pytest.fixture(scope='module')
def connection():
    try:
        # Establish a connection to the database
        connection = get_database_connection()
        yield connection
    except OperationalError as e:
        pytest.fail(f"Unable to connect to the database: {e}")
    finally:
        connection.close()

def test_database_connection(connection):
    # Test query to check the connection
    result = connection.execute(text("SELECT 'Hello, world!'"))
    for row in result:
        assert row[0] == 'Hello, world!'