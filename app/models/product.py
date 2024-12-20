from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel


class Product(BaseModel):
    """
    Represents a product in the application.

    Attributes:
        product_id (int): Primary key identifier for the product.
        product_name (str): The unique name of the product.
        product_amount (float): The price or amount associated with the product.
    """

    __tablename__ = "products"

    product_id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key identifier for the product."
    )
    product_name = Column(
        String,
        nullable=False,
        unique=True,
        doc="The unique name of the product. Cannot be null."
    )
    product_amount = Column(
        Float,
        nullable=False,
        doc="The price or amount associated with the product. Cannot be null."
    )

    @validates("product_name")
    def validate_product_name(self, key, value):
        """
        Validate the product name to ensure it is not empty and has valid characters.

        Args:
            key (str): The field being validated.
            value (str): The value to validate.

        Returns:
            str: The validated product name.

        Raises:
            ValueError: If the product name is empty or too short.
        """
        if not value or not value.strip():
            raise ValueError("Product name cannot be empty or blank.")
        if len(value) < 3:
            raise ValueError("Product name must be at least 3 characters long.")
        return value.strip()

    @validates("product_amount")
    def validate_product_amount(self, key, value):
        """
        Validate the product amount to ensure it is a positive number.

        Args:
            key (str): The field being validated.
            value (float): The value to validate.

        Returns:
            float: The validated product amount.

        Raises:
            ValueError: If the product amount is not positive.
        """
        if value is None or value <= 0:
            raise ValueError("Product amount must be a positive number.")
        return value
