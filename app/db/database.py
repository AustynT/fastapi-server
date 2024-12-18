from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the database URL from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure the DATABASE_URL is provided
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Initialize the SQLAlchemy engine
# Use `pool_pre_ping=True` to check if connections are alive
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency for FastAPI to manage the session lifecycle
def get_db():
    """
    Dependency to get the database session.
    Ensures that the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
