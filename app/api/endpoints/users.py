from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.dependency import get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserResponse
from app.models.user import User

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a list of all users.
    """
    user_service = UserService(db)
    return user_service.get_all_users()


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a user by ID.
    """
    user_service = UserService(db)
    return user_service.get_user_by_id(user_id)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a user by ID.
    """
    user_service = UserService(db)
    return user_service.delete_user_by_id(user_id)