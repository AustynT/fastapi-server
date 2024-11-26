import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_NAME = os.getenv("APP_NAME", "FastAPI App")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    ENV = os.getenv("ENV", "development")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")


    DATABASE_URL = os.getenv("DATABASE_URL")



config = Config()