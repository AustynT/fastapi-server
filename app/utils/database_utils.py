from sqlalchemy.orm import Session
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
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def commit_and_refresh(self, instance):
        """
        Commit the current transaction and refresh the given instance.
        """
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get_instance_by_id(self, model, id: int):
        """
        Retrieve an instance of a model by its ID.
        """
        instance = self.db.query(model).filter(model.id == id).first()
        if not instance:
            raise HTTPException(status_code=404, detail=f"{model.__name__} with ID {id} not found")
        return instance

    def delete_and_commit(self, instance):
        """
        Delete an instance from the database and commit the session.
        """
        self.db.delete(instance)
        self.db.commit()

    def find_and_update(self, model, id: int, updated_data: dict):
        """
        Find a record by ID, update its attributes, and commit the changes.
        """
        instance = self.get_instance_by_id(model, id)
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
            instance = self.get_instance_by_id(model, id)
            for key, value in update_data.items():
                setattr(instance, key, value)
            updated_instances.append(self.commit_and_refresh(instance))
        return updated_instances
