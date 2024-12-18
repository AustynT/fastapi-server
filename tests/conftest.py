import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.db.database import Base, get_db
from app.main import app

# Load environment variables
load_dotenv()

# Ensure the project root is in the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load Test Database URL from .env
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise ValueError(
        "TEST_DATABASE_URL is not set in the .env file. "
        "Please add it in the format 'postgresql://username:password@localhost/dbname'"
    )

# PostgreSQL test database engine setup
try:
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"options": "-c timezone=UTC"}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    raise RuntimeError(f"Failed to create test database engine: {e}")

# Override the get_db dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture for creating a fresh test database and cleaning it up
@pytest.fixture(scope="function")
def db():
    """
    Provides a fresh database session for each test function.
    """
    try:
        print("Setting up test database: dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        print("Creating test database tables...")
        Base.metadata.create_all(bind=engine)
        db_session = TestingSessionLocal()
        yield db_session  # Provide the session to the test
    except Exception as e:
        print(f"Error during test database setup: {e}")
        raise
    finally:
        print("Tearing down test database: closing session and dropping tables...")
        db_session.close()
        Base.metadata.drop_all(bind=engine)
        print("Test database teardown complete.")


# Fixture for the FastAPI TestClient
@pytest.fixture(scope="module")  # Change scope to 'function' for isolated clients per test
def test_client():
    """
    Provides a TestClient for testing FastAPI endpoints.
    """
    with TestClient(app) as client:
        yield client
