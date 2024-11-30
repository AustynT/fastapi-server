from sqlalchemy.orm import Session
from fastapi import HTTPException


def add_and_commit(db: Session, instance):
    """
    Add an instance to the database, commit the session, and refresh the instance.
    
    Args:
        db (Session): SQLAlchemy database session.
        instance: SQLAlchemy model instance to add.

    Returns:
        The added and refreshed instance.
    """
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def commit_and_refresh(db: Session, instance):
    """
    Commit the current transaction and refresh the given instance.

    Args:
        db (Session): SQLAlchemy database session.
        instance: SQLAlchemy model instance to refresh.

    Returns:
        The refreshed instance.
    """
    db.commit()
    db.refresh(instance)
    return instance


def get_instance_by_id(db: Session, model, id: int):
    """
    Retrieve an instance of a model by its ID.
    
    Args:
        db (Session): SQLAlchemy database session.
        model: SQLAlchemy model class.
        id (int): ID of the record to retrieve.

    Returns:
        The retrieved instance or raises HTTPException if not found.
    """
    instance = db.query(model).filter(model.id == id).first()
    if not instance:
        raise HTTPException(status_code=404, detail=f"{model.__name__} with ID {id} not found")
    return instance


def delete_and_commit(db: Session, instance):
    """
    Delete an instance from the database and commit the session.

    Args:
        db (Session): SQLAlchemy database session.
        instance: SQLAlchemy model instance to delete.

    Returns:
        None
    """
    db.delete(instance)
    db.commit()


def find_and_update(db: Session, model, id: int, updated_data: dict):
    """
    Find a record by ID, update its attributes, and commit the changes.
    
    Args:
        db (Session): SQLAlchemy database session.
        model: SQLAlchemy model class.
        id (int): ID of the record to update.
        updated_data (dict): Dictionary containing fields to update.

    Returns:
        The updated and refreshed instance.
    """
    instance = get_instance_by_id(db, model, id)
    for key, value in updated_data.items():
        setattr(instance, key, value)
    return commit_and_refresh(db, instance)


def bulk_update(db: Session, model, updates: list[dict]):
    """
    Bulk update multiple records in the database.

    Args:
        db (Session): SQLAlchemy database session.
        model: SQLAlchemy model class.
        updates (list[dict]): List of dictionaries containing IDs and fields to update.

    Returns:
        List of updated instances.
    """
    updated_instances = []
    for update_data in updates:
        id = update_data.pop("id", None)
        if not id:
            raise HTTPException(status_code=400, detail="Missing ID for bulk update")
        instance = get_instance_by_id(db, model, id)
        for key, value in update_data.items():
            setattr(instance, key, value)
        updated_instances.append(commit_and_refresh(db, instance))
    return updated_instances
