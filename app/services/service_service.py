from app.services.base_service import BaseService
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate
from fastapi import HTTPException

class ServiceService(BaseService):
    def get_all_services(self):
        """
        Retrieve all services from the database.
        """
        return self._database.get_all(Service)

    def get_service_by_id(self, service_id: int):
        """
        Retrieve a single service by its ID.
        """
        service = self._database.get_by_id(Service, service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return service

    def create_service(self, service_data: ServiceCreate):
        """
        Create a new service and save it to the database.
        """
        new_service = Service(**service_data.dict())
        return self._database.add_and_commit(new_service)

    def update_service(self, service_id: int, updated_data: ServiceUpdate):
        """
        Update an existing service by its ID.
        """
        service = self._database.get_by_id(Service, service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(service, key, value)
        return self._database.commit_and_refresh(service)

    def delete_service(self, service_id: int):
        """
        Delete a service by its ID.
        """
        service = self._database.get_by_id(Service, service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        self._database.delete_and_commit(service)
        return {"message": "Service deleted successfully"}
