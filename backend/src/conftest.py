import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.models.base import Base
from fastapi.testclient import TestClient
from main import app
from db.dependencies import get_db

# These fixtures are available for all tests

DATABASE_URL = f'postgresql://dev_user:dev_password@localhost:5432/unmatched_test'
engine = create_engine(DATABASE_URL)

@pytest.fixture(scope='module')
def test_engine():
    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def test_session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()

    yield session

    session.rollback()

    for table in reversed(Base.metadata.sorted_tables):
      session.execute(text(f'TRUNCATE {table.name} CASCADE;'))
      session.commit()

    session.close()

@pytest.fixture(scope='function')
def client(test_session):
    app.dependency_overrides[get_db] = lambda: test_session
    with TestClient(app) as c:
        yield c