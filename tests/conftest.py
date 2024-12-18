import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.db.database import Base, get_db  # Your database models and dependency
from app.main import app  # Your FastAPI app entry point

# Load environment variables
load_dotenv()

# Load Test Database URL from .env
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL is not set in .env file")

# PostgreSQL test database engine setup
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture for creating and tearing down the test database
@pytest.fixture(scope="module")
def test_client():
    """
    Creates a TestClient and manages the lifecycle of the test database.
    """
    # Create tables in the test database before tests
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client  # Yield the client for testing
    # Drop all tables after the tests complete
    Base.metadata.drop_all(bind=engine)
