from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class UserService(BaseModel):
    """
    Represents user-specific service offerings tied to service pricing.

    Attributes:
        id (int): Primary key identifier.
        user_id (int): Foreign key referencing the user.
        service_id (int): Foreign key referencing the service.
        service_pricing_id (int): Foreign key referencing the service pricing.
        availability (bool): Indicates whether the service is available.
    """

    __tablename__ = "user_services"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier."
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        doc="Foreign key referencing the user."
    )
    service_id = Column(
        Integer,
        ForeignKey("services.service_id"),
        nullable=False,
        doc="Foreign key referencing the service."
    )
    service_pricing_id = Column(
        Integer,
        ForeignKey("service_pricing.id"),
        nullable=False,
        doc="Foreign key referencing the service pricing."
    )
    availability = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates whether the service is available."
    )

    user = relationship("User", back_populates="services")
    service = relationship("Service", back_populates="users")
    pricing = relationship("ServicePricing", back_populates="user_services")
