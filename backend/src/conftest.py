import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models.base import Base

# These fixtures are available for all tests

@pytest.fixture(scope='module')
def test_engine():
    DATABASE_URL = f'postgresql://dev_user:dev_password@localhost:5432/unmatched_test'
    
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope='function')
def test_session(test_engine):
    # Drop and recreate all tables before each test
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)

    Session = sessionmaker(bind=test_engine)
    session = Session()

    yield session

    # Rollback the transaction after each test
    session.close()