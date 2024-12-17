import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from app.main import app

# Test database setup (SQLite in-memory for simplicity)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Pytest fixture for test client
@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)  # Create tables
    with TestClient(app) as client:
        yield client
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests
