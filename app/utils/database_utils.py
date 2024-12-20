from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

class DatabaseUtils:
    def __init__(self, db: Session):
        """
        Initialize the DatabaseUtils with a SQLAlchemy session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def add_and_commit(self, instance):
        """
        Add an instance to the database, commit the session, and refresh the instance.
        """
        try:
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def add_all_and_commit(self, instances):
        """
        Add multiple instances to the database and commit.
        """
        try:
            self.db.add_all(instances)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def bulk_add(self, instances):
        """
        Add multiple instances to the database without committing.
        """
        try:
            self.db.add_all(instances)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def commit_and_refresh(self, instance):
        """
        Commit the current transaction and refresh the given instance.
        """
        try:
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_by_id(self, model, id: int):
        """
        Retrieve an instance of a model by its ID.
        """
        instance = self.db.query(model).filter(model.id == id).first()
        if not instance:
            raise HTTPException(status_code=404, detail=f"{model.__name__} with ID {id} not found")
        return instance

    def get_by_string(self, model, field_name: str, value: str):
        """
        Retrieve an instance of a model by a string field.

        Args:
            model: SQLAlchemy model class.
            field_name (str): Name of the string field to filter by.
            value (str): Value to search for in the specified field.

        Returns:
            The retrieved instance or raises an HTTPException if not found.
        """
        if not hasattr(model, field_name):
            raise HTTPException(status_code=400, detail=f"Invalid field: {field_name} for {model.__name__}")

        instance = self.db.query(model).filter(getattr(model, field_name) == value).first()
        if not instance:
            raise HTTPException(status_code=404, detail=f"{model.__name__} with {field_name} '{value}' not found")
        return instance

    def find_or_404(self, model, **filters):
        """
        Retrieve an instance of a model based on filters or raise a 404 error if not found.

        Args:
            model: SQLAlchemy model class.
            **filters: Field-value pairs to filter by.

        Returns:
            The retrieved instance if found.

        Raises:
            HTTPException: If the instance does not exist.
        """
        instance = self.db.query(model).filter_by(**filters).first()
        if not instance:
            filter_details = ", ".join(f"{key}={value}" for key, value in filters.items())
            raise HTTPException(
                status_code=404,
                detail=f"{model.__name__} with {filter_details} not found"
            )
        return instance

    def get_all(self, model):
        """
        Retrieve all instances of a model from the database.
        """
        return self.db.query(model).all()

    def delete_and_commit(self, instance):
        """
        Delete an instance from the database and commit the session.
        """
        try:
            self.db.delete(instance)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def find_and_update(self, model, id: int, updated_data: dict):
        """
        Find a record by ID, update its attributes, and commit the changes.
        """
        instance = self.get_by_id(model, id)
        for key, value in updated_data.items():
            setattr(instance, key, value)
        return self.commit_and_refresh(instance)

    def bulk_update(self, model, updates: list[dict]):
        """
        Bulk update multiple records in the database.
        """
        updated_instances = []
        for update_data in updates:
            id = update_data.pop("id", None)
            if not id:
                raise HTTPException(status_code=400, detail="Missing ID for bulk update")
            instance = self.get_by_id(model, id)
            for key, value in update_data.items():
                setattr(instance, key, value)
            updated_instances.append(self.commit_and_refresh(instance))
        return updated_instances
