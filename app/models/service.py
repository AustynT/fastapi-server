from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel

class Service(BaseModel):
    """
    Represents a service offered by the application.

    Attributes:
        service_id (int): Primary key identifier for the service.
        service_name (str): The unique name of the service.
        total_amount (float): The total amount or cost of the service.
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
    total_amount = Column(
        Float,
        nullable=False,
        doc="The total amount or cost of the service. Cannot be null."
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

    @validates("total_amount")
    def validate_total_amount(self, key, value):
        """
        Validate the total amount to ensure it is a positive number.

        Args:
            key (str): The field being validated.
            value (float): The value to validate.

        Returns:
            float: The validated total amount.

        Raises:
            ValueError: If the total amount is not positive.
        """
        if value is None or value <= 0:
            raise ValueError("Total amount must be a positive number.")
        return value
