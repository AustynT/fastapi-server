from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class UserServiceMapping(BaseModel):
    """
    Represents the mapping between users and services they provide.

    Attributes:
        id (int): Primary key identifier.
        user_id (int): Foreign key referencing the user.
        service_id (int): Foreign key referencing the service.
        service_pricing_id (int): Foreign key referencing the service pricing.
        availability (bool): Indicates if the service is available from this user.
    """

    __tablename__ = "user_service_mapping"

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
        nullable=True,
        doc="Foreign key referencing the service pricing."
    )
    availability = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates if the service is available from this user."
    )

    user = relationship(
        "User",
        back_populates="provided_services",
        doc="Relationship to the User model."
    )
    service = relationship(
        "Service",
        back_populates="user_services",
        doc="Relationship to the Service model."
    )
    service_pricing = relationship(
        "ServicePricing",
        back_populates="user_service_mappings",
        doc="Relationship to the ServicePricing model for pricing details."
    )
