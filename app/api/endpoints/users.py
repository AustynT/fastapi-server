from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/users", response_model=List[dict])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/users", response_model=dict)
async def create_user(user_data: dict, db: Session = Depends(get_db)):
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: int, updated_data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
