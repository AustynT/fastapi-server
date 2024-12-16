from sqlalchemy.orm import Session
from app.utils.database_utils import DatabaseUtils

class BaseService:
    def __init__(self, db: Session):
        self.database_utils = DatabaseUtils(db)
