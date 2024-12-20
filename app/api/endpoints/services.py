from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.dependency import get_current_user
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse, ServiceListResponse
from app.services.service_service import ServiceService
from app.models.user import User

router = APIRouter()

@router.get("/services", response_model=ServiceListResponse)
async def get_services(db: Session = Depends(get_db)):
    """
    Get all services.
    """
    service_service = ServiceService(db)
    services = service_service.get_all_services()
    return {"services": services}

@router.get("/services/{service_id}", response_model=ServiceResponse)
async def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    """
    Get a service by its ID.
    """
    service_service = ServiceService(db)
    return service_service.get_service_by_id(service_id)

@router.post("/services", response_model=ServiceResponse, status_code=201)
async def create_service(
    service_data: ServiceCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    """
    Create a new service.
    """
    service_service = ServiceService(db)
    return service_service.create_service(service_data)

@router.put("/services/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int, 
    updated_data: ServiceUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    """
    Update an existing service by its ID.
    """
    service_service = ServiceService(db)
    return service_service.update_service(service_id, updated_data)

@router.delete("/services/{service_id}")
async def delete_service(
    service_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    """
    Delete a service by its ID.
    """
    service_service = ServiceService(db)
    return service_service.delete_service(service_id)
