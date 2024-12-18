import pytest
from sqlalchemy.orm import Session 
from app.db.database import Base

class BaseModelTest:
    """
    Base Test class for models to provice reusable setup/teardown logic.
    """
    
    @pytest.fixture(autouse=True, scope="function")
    def setup_and_teardown(self, db: Session):
        # Clear the database tables before and after each test
        
        Base.metadata.drop_all(bind=db.bind)
        Base.metadata.create_all(bind=db.bind)
        yield
        Base.metadata.drop_all(bind=db.bind)