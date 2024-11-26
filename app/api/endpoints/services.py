from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.service import Service

router = APIRouter()

@router.get("/services", response_model=List[dict])
async def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()

@router.post("/services", response_model=dict)
async def create_service(service_data: dict, db: Session = Depends(get_db)):
    new_service = Service(**service_data)
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@router.put("/services/{service_id}", response_model=dict)
async def update_service(service_id: int, updated_data: dict, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    for key, value in updated_data.items():
        setattr(service, key, value)
    db.commit()
    db.refresh(service)
    return service

@router.delete("/services/{service_id}")
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
    return {"message": "Service deleted successfully"}