from sqlalchemy.orm import Session
from app.utils.database_utils import DatabaseUtils as _database

class BaseService:
    def __init__(self, db: Session):
        """
        Initialize the service with a database session and utilities.
        """
        self._database = _database(db)
