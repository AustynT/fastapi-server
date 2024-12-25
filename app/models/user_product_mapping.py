from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class UserProductMapping(BaseModel):
    """
    Represents the mapping between users and products they sell.

    Attributes:
        id (int): Primary key identifier.
        user_id (int): Foreign key referencing the user.
        product_id (int): Foreign key referencing the product.
        product_pricing_id (int): Foreign key referencing the product pricing.
        availability (bool): Indicates if the product is available from this user.
    """

    __tablename__ = "user_product_mapping"

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
        nullable=True,
        doc="Foreign key referencing the product pricing."
    )
    availability = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates if the product is available from this user."
    )

    user = relationship(
        "User",
        back_populates="provided_products",
        doc="Relationship to the User model."
    )
    product = relationship(
        "Product",
        back_populates="user_products",
        doc="Relationship to the Product model."
    )
    product_pricing = relationship(
        "ProductPricing",
        back_populates="user_product_mappings",
        doc="Relationship to the ProductPricing model for pricing details."
    )
