from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.dependency import get_current_user
from app.models.job_history import JobHistory
from app.models.user import User
from app.schemas.job_history import JobHistoryResponse
router = APIRouter()

@router.get("/job-history/{user_id}", response_model=JobHistoryResponse)
async def get_user_jobs(
        user_id: int,
        db: Session = Depends(get_db), 
        current_user: User = Depends(get_current_user)):
    
    pass