from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.dependency import get_current_user
from app.models.job_history import JobHistory
from app.models.user import User
from app.schemas.job_history import JobHistoryResponse, JobHistoryRequest
router = APIRouter()

@router.get("/job-history", response_model=List[JobHistoryResponse])
async def get_user_jobs(
        user_id: int,
        db: Session = Depends(get_db), 
    ):        
    
    user_jobs = db.query(JobHistory).filter(JobHistory.user_id == user_id).all()
    
    if not user_jobs:
        raise HTTPException(status_code=404, detail="No Job History Found for this user")
    
    return user_jobs

@router.post("/create-job-history", response_model=JobHistoryResponse)
async def create_job_history(job_history_data: JobHistoryRequest, 
                             db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_user)):
    pass


@router.put('/edit-job-history/{job_history_id}', response_model=JobHistoryResponse)
async def edit_job_history(job_data: JobHistoryRequest,
                           db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    pass

@router.delete("/delete-job-history/{job_history_id}")
async def delete_job_history():
    pass