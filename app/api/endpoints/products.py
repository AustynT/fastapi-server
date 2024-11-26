from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.product import Product

router = APIRouter()

@router.get("/products", response_model=List[dict])
async def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.post("/products", response_model=dict)
async def create_product(product_data: dict, db: Session = Depends(get_db)):
    new_product = Product(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/products/{product_id}", response_model=dict)
async def update_product(product_id: int, updated_data: dict, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in updated_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
