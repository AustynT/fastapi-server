from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class ServiceBase(BaseModel):
    """
    Shared fields for Service schema.
    """
    service_name: str = Field(..., max_length=255, description="The name of the service.")
    total_amount: float = Field(..., gt=0, description="The total amount or cost of the service.")

class ServiceCreate(ServiceBase):
    """
    Fields required for creating a new service.
    """
    pass

class ServiceUpdate(BaseModel):
    """
    Fields that can be updated for a service.
    """
    service_name: Optional[str] = Field(None, max_length=255, description="The updated name of the service.")
    total_amount: Optional[float] = Field(None, gt=0, description="The updated total amount or cost of the service.")

class ServiceResponse(ServiceBase):
    """
    Fields returned in the API response for a single service.
    """
    service_id: int = Field(..., description="The unique identifier for the service.")

    model_config = ConfigDict(
        from_attributes=True,  # Ensures the model can be populated from ORM objects
        json_schema_extra={
            "example": {
                "service_id": 1,
                "service_name": "Website Development",
                "total_amount": 2500.00,
            }
        },
    )

class ServiceListResponse(BaseModel):
    """
    Fields returned in the API response for a list of services.
    """
    services: List[ServiceResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "services": [
                    {"service_id": 1, "service_name": "Website Development", "total_amount": 2500.00},
                    {"service_id": 2, "service_name": "SEO Optimization", "total_amount": 1200.00},
                ]
            }
        },
    )
