import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from db.database import get_db
from db.models.base import Base
from factories.b_factory import BaseFactory
from main import app


# Passes session to all factories
def set_session_factory_for_all_subclasses(session):
    def set_session_factory(factory_cls, session):
        factory_cls._meta.sqlalchemy_session_factory = lambda: session

    for subclass in BaseFactory.__subclasses__():
        set_session_factory(subclass, session)
        for subsubclass in subclass.__subclasses__():
            set_session_factory(subsubclass, session)


@pytest.fixture(scope="module")
def test_engine():
    DATABASE_URL = "postgresql://dev_user:dev_password@localhost:5432/unmatched_test"
    engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_engine):
    session_local = sessionmaker(bind=test_engine)
    session = session_local()
    set_session_factory_for_all_subclasses(session)

    yield session

    session.rollback()

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(text(f"TRUNCATE {table.name} CASCADE;"))
        session.commit()

    session.close()


@pytest.fixture(scope="function")
def client(test_session):
    app.dependency_overrides[get_db] = lambda: test_session
    with TestClient(app) as c:
        yield c
