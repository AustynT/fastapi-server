from sqlalchemy import Column, Float, Integer, String, ForeignKey
from app.models.base_model import BaseModel


class Product(BaseModel):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key = True, index = True)
  
    product_name = Column(String, nullable = False, unique=True)
    product_amount = Column(Float, nullable=False)

