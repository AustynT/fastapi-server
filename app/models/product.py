from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Product(BaseModel):
    """
    Represents a product offered by the application.

    Attributes:
        product_id (int): Primary key identifier for the product.
        product_name (str): The unique name of the product.
        description (str): A brief description of the product.
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
        unique=True,
        nullable=False,
        doc="The unique name of the product. Cannot be null."
    )
    description = Column(
        String,
        nullable=True,
        doc="A brief description of the product."
    )

    services_included = relationship(
        "ServiceProduct",
        back_populates="product",
        doc="Relationship to ServiceProduct for services included in this product."
    )
    products_included = relationship(
        "ProductService",
        back_populates="product",
        doc="Relationship to ProductService for products included in services."
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
