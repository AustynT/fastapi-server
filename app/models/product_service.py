from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class ProductService(BaseModel):
    """
    Represents the relationship where a product is included in a service.

    Attributes:
        id (int): Primary key identifier.
        product_id (int): Foreign key referencing the product.
        service_id (int): Foreign key referencing the service.
    """

    __tablename__ = "product_services"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the product-service relationship."
    )
    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False,
        doc="Foreign key referencing the product."
    )
    service_id = Column(
        Integer,
        ForeignKey("services.service_id"),
        nullable=False,
        doc="Foreign key referencing the service."
    )

    product = relationship(
        "Product",
        back_populates="services_included",
        doc="Relationship to the Product model for the included product."
    )
    service = relationship(
        "Service",
        back_populates="products_included",
        doc="Relationship to the Service model for the associated service."
    )

    service_pricing = relationship(
        "ServicePricing",
        primaryjoin="ProductService.service_id == ServicePricing.service_id",
        back_populates="product_services",
        doc="Relationship to the ServicePricing model for the service's pricing details."
    )
