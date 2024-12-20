from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class ProductBase(BaseModel):
    """
    Shared fields for Product schema.
    """
    product_name: str = Field(..., max_length=255, description="The name of the product.")
    product_amount: float = Field(..., gt=0, description="The amount or price of the product.")

class ProductCreate(ProductBase):
    """
    Fields required for creating a new product.
    """
    pass

class ProductUpdate(BaseModel):
    """
    Fields that can be updated for a product.
    """
    product_name: Optional[str] = Field(None, max_length=255, description="The updated name of the product.")
    product_amount: Optional[float] = Field(None, gt=0, description="The updated amount or price of the product.")

class ProductResponse(ProductBase):
    """
    Fields returned in the API response for a single product.
    """
    product_id: int = Field(..., description="The unique identifier for the product.")

    model_config = ConfigDict(
        from_attributes=True,  # Ensures the model can be populated from ORM objects
        json_schema_extra={
            "example": {
                "product_id": 1,
                "product_name": "Smartphone",
                "product_amount": 699.99,
            }
        },
    )

class ProductListResponse(BaseModel):
    """
    Fields returned in the API response for a list of products.
    """
    products: List[ProductResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "products": [
                    {"product_id": 1, "product_name": "Smartphone", "product_amount": 699.99},
                    {"product_id": 2, "product_name": "Laptop", "product_amount": 1199.99},
                ]
            }
        },
    )
