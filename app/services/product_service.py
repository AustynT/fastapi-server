from app.services.base_service import BaseService
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException

class ProductService(BaseService):
    def get_all_products(self):
        """
        Retrieve all products from the database.
        """
        return self._database.get_all(Product)

    def get_product_by_id(self, product_id: int):
        """
        Retrieve a single product by its ID.
        """
        product = self._database.get_by_id(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def create_product(self, product_data: ProductCreate):
        """
        Create a new product and save it to the database.
        """
        new_product = Product(**product_data.dict())
        return self._database.add_and_commit(new_product)

    def update_product(self, product_id: int, updated_data: ProductUpdate):
        """
        Update an existing product by its ID.
        """
        product = self._database.get_by_id(Product, product_id)
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        return self._database.commit_and_refresh(product)

    def delete_product(self, product_id: int):
        """
        Delete a product by its ID.
        """
        product = self._database.get_by_id(Product, product_id)
        self._database.delete_and_commit(product)
        return {"message": "Product deleted successfully"}
