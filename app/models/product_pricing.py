from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class ProductPricing(BaseModel):
    """
    Represents pricing rules for products.

    Attributes:
        id (int): Primary key identifier for the pricing rule.
        product_id (int): Foreign key referencing the product.
        rule_name (str): Name of the pricing rule.
        amount (float): Monetary value of the rule.
        rule_type (str): Type of the rule (e.g., base, additional, discount).
    """

    __tablename__ = "product_pricing"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the pricing rule."
    )
    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False,
        doc="Foreign key referencing the product."
    )
    rule_name = Column(
        String,
        nullable=False,
        doc="Name of the pricing rule (e.g., base price, discount)."
    )
    amount = Column(
        Float,
        nullable=False,
        doc="Monetary value of the pricing rule."
    )
    rule_type = Column(
        Enum("base", "additional", "discount", name="product_rule_type"),
        nullable=False,
        doc="Type of the rule (e.g., base, additional, discount)."
    )

    product = relationship(
        "Product",
        back_populates="pricing"
    )

    service_products = relationship(
        "ServiceProduct",
        back_populates="product_pricing",
        doc="Relationship to ServiceProduct for products that include services."
    )