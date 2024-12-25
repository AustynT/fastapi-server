from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class UserProduct(BaseModel):
    """
    Represents user-specific product offerings tied to product pricing.

    Attributes:
        id (int): Primary key identifier.
        user_id (int): Foreign key referencing the user.
        product_id (int): Foreign key referencing the product.
        product_pricing_id (int): Foreign key referencing the product pricing.
        availability (bool): Indicates whether the product is available.
    """

    __tablename__ = "user_products"

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
    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False,
        doc="Foreign key referencing the product."
    )
    product_pricing_id = Column(
        Integer,
        ForeignKey("product_pricing.id"),
        nullable=False,
        doc="Foreign key referencing the product pricing."
    )
    availability = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates whether the product is available."
    )

    user = relationship("User", back_populates="products")
    product = relationship("Product", back_populates="users")
    pricing = relationship("ProductPricing", back_populates="user_products")
