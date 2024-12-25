from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from app.models.base_model import BaseModel

class Service(BaseModel):
    """
    Represents a service offered by the application.

    Attributes:
        service_id (int): Primary key identifier for the service.
        service_name (str): The unique name of the service.
        description (str): A brief description of the service.
    """

    __tablename__ = "services"

    service_id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the service."
    )
    service_name = Column(
        String,
        unique=True,
        nullable=False,
        doc="The unique name of the service. Cannot be null."
    )
    description = Column(
        String,
        nullable=True,
        doc="A brief description of the service."
    )

    products_included = relationship(
        "ProductService",
        back_populates="service",
        doc="Relationship to ProductService for products included in this service."
    )
    services_included = relationship(
        "ServiceProduct",
        back_populates="service",
        doc="Relationship to ServiceProduct for services included in products."
    )


    @validates("service_name")
    def validate_service_name(self, key, value):
        """
        Validate the service name to ensure it is not empty and has valid characters.

        Args:
            key (str): The field being validated.
            value (str): The value to validate.

        Returns:
            str: The validated service name.

        Raises:
            ValueError: If the service name is empty or too short.
        """
        if not value or not value.strip():
            raise ValueError("Service name cannot be empty or blank.")
        if len(value) < 3:
            raise ValueError("Service name must be at least 3 characters long.")
        return value.strip()
