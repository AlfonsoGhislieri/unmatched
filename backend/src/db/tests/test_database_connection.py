import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from db.database import get_database_session

import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from db.database import get_database_session

@pytest.fixture(scope='module')
def session():
    try:
        session = get_database_session()
        yield session
    except OperationalError as e:
        pytest.fail(f"Unable to connect to the database: {e}")
    finally:
        session.close()

def test_database_connection(session):
    # Test query to check the connection
    result = session.execute(text("SELECT 'Hello, world!'"))
    for row in result:
        assert row[0] == 'Hello, world!'