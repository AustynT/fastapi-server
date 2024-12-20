from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.dependency import get_current_user
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from app.models.user import User
from app.services.product_service import ProductService

router = APIRouter()

@router.get("/products", response_model=ProductListResponse)
async def get_products(
    db: Session = Depends(get_db)):
    """
    Get all products.
    """
    product_service = ProductService(db)
    products = product_service.get_all_products()
    return {"products": products}

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: int, 
    db: Session = Depends(get_db)):
    """
    Get a product by its ID.
    """
    product_service = ProductService(db)
    return product_service.get_product_by_id(product_id)

@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    """
    Create a new product.
    """
    product_service = ProductService(db)
    return product_service.create_product(product_data)

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int, 
    updated_data: ProductUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    """
    Update an existing product by ID.
    """
    product_service = ProductService(db)
    return product_service.update_product(product_id, updated_data)

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):
    """
    Delete a product by ID.
    """
    product_service = ProductService(db)
    return product_service.delete_product(product_id)
