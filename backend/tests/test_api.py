import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.jobs import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})
TestingSessionLocally = sessionmaker(autocommit = False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocally()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

