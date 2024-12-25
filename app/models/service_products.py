from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class ServiceProduct(BaseModel):
    """
    Represents the relationship where a service is included in a product.

    Attributes:
        id (int): Primary key identifier.
        service_id (int): Foreign key referencing the service.
        product_id (int): Foreign key referencing the product.
    """

    __tablename__ = "service_products"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the service-product relationship."
    )
    service_id = Column(
        Integer,
        ForeignKey("services.service_id"),
        nullable=False,
        doc="Foreign key referencing the service."
    )
    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False,
        doc="Foreign key referencing the product."
    )

    service = relationship(
        "Service",
        back_populates="services_included",
        doc="Relationship to the Service model for the included service."
    )
    product = relationship(
        "Product",
        back_populates="products_included",
        doc="Relationship to the Product model for the associated product."
    )

    product_pricing = relationship(
        "ProductPricing",
        primaryjoin="ServiceProduct.product_id == ProductPricing.product_id",
        back_populates="service_products",
        doc="Relationship to the ProductPricing model for the product's pricing details."
    )
