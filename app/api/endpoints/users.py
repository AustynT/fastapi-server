from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.dependency import get_current_user
from app.utils.database_utils import get_instance_by_id, delete_and_commit
from app.models.user import User
from app.schemas.users import UserResponse

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_users(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    """
    Get a list of all users.
    """
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.
    """
    return get_instance_by_id(db, User, user_id)

@router.delete("/users/{user_id}")
async def delete_user(
        user_id: int, 
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    """
    Delete a user by ID.
    """
    user = get_instance_by_id(db, User, user_id)
    delete_and_commit(db, user)
    return {"message": "User deleted successfully"}
