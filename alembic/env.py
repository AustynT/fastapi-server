import sys
import os
from logging.config import fileConfig
from alembic import context
from app.db.database import Base  # Import your Base metadata
from app.models import user # Import your models
from dotenv import load_dotenv

# Add the alembic folder to the Python path
sys.path.append(os.path.dirname(__file__))

# Import utilities after adding alembic to the path
from migrations_utils import run_migrations_offline, run_migrations_online

# Load environment variables from .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Alembic Config Object
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your models' metadata here
target_metadata = Base.metadata

# Determine offline or online mode and call the appropriate function
if context.is_offline_mode():
    run_migrations_offline(target_metadata)
else:
    run_migrations_online(target_metadata)
