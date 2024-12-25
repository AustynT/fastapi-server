from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class ServicePricing(BaseModel):
    """
    Represents pricing rules for services.

    Attributes:
        id (int): Primary key identifier for the pricing rule.
        service_id (int): Foreign key referencing the service.
        rule_name (str): Name of the pricing rule.
        amount (float): Monetary value of the rule.
        rule_type (str): Type of the rule (e.g., base, additional, discount).
    """

    __tablename__ = "service_pricing"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the pricing rule."
    )
    service_id = Column(
        Integer,
        ForeignKey("services.service_id"),
        nullable=False,
        doc="Foreign key referencing the service."
    )
    rule_name = Column(
        String,
        nullable=False,
        doc="Name of the pricing rule (e.g., base fee, setup charge)."
    )
    amount = Column(
        Float,
        nullable=False,
        doc="Monetary value of the pricing rule."
    )
    rule_type = Column(
        Enum("base", "additional", "discount", name="service_rule_type"),
        nullable=False,
        doc="Type of the rule (e.g., base, additional, discount)."
    )

    service = relationship(
        "Service", 
        back_populates="pricing"
    )
    
    product_services = relationship(
        "ProductService",
        back_populates="service_pricing",
        doc="Relationship to ProductService for services that include products."
    )
