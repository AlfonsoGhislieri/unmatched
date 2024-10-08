import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from testcontainers.postgres import PostgresContainer

from db.database import get_session_engine


@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        postgres.start()
        yield postgres


@pytest.fixture(scope="module")
def db_resources(postgres_container):
    Session, engine = get_session_engine(postgres_container.get_connection_url())
    return Session, engine


@pytest.fixture(scope="module")
def session(db_resources):
    Session, _ = db_resources
    session = Session()
    try:
        yield session
        session.commit()
    except OperationalError as e:
        pytest.fail(f"Unable to connect to the database: {e}")
    except Exception as e:
        session.rollback()
        pytest.fail(f"An error occurred: {e}")
    finally:
        session.close()


def test_database_connection(session):
    # Test query to check the connection
    try:
        result = session.execute(text("SELECT 'Hello, world!'"))
        for row in result:
            assert row[0] == "Hello, world!"
    except OperationalError as e:
        pytest.fail(f"Unable to execute the query: {e}")


def test_engine_connection(db_resources):
    _, engine = db_resources
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 'Hello, world!'"))
            for row in result:
                assert row[0] == "Hello, world!"
    except OperationalError as e:
        pytest.fail(f"Unable to connect to the database: {e}")
