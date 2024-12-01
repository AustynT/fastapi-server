from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.utils.database_utils import add_and_commit, find_and_update, get_instance_by_id, delete_and_commit
from app.models.user import User

router = APIRouter()

@router.get("/users", response_model=List[dict])
async def get_users(db: Session = Depends(get_db)):
    """
    Get a list of all users.
    """
    return db.query(User).all()

@router.post("/users", response_model=dict)
async def create_user(user_data: dict, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    new_user = User(**user_data)
    return add_and_commit(db, new_user)

@router.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: int, updated_data: dict, db: Session = Depends(get_db)):
    """
    Update an existing user by ID.
    """
    return find_and_update(db, User, user_id, updated_data)

@router.get("/users/{user_id}", response_model=dict)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.
    """
    return get_instance_by_id(db, User, user_id)

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.
    """
    user = get_instance_by_id(db, User, user_id)
    delete_and_commit(db, user)
    return {"message": "User deleted successfully"}
