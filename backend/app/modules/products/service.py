from sqlalchemy.orm import Session

from app.modules.products.model import Product
from app.modules.products.repository import product_repository
from app.modules.products.schema import ProductCreate, ProductUpdate


class ProductService:

    def create_product(
        self,
        db: Session,
        product: ProductCreate,
    ) -> Product:
        print("Service create_product() called")
        existing_product = product_repository.get_by_sku(
            db,
            product.sku,
        )

        if existing_product:
            raise ValueError("Product with this SKU already exists.")

        if product.selling_price < product.purchase_price:
            raise ValueError(
                "Selling price cannot be less than purchase price."
            )

        return product_repository.create(db, product)

    def get_all_products(self, db: Session):
        return product_repository.get_all(db)

    def get_product_by_id(
        self,
        db: Session,
        product_id: int,
    ):

        product = product_repository.get_by_id(
            db,
            product_id,
        )

        if not product:
            raise ValueError("Product not found.")

        return product

    def update_product(
        self,
        db: Session,
        product_id: int,
        product: ProductUpdate,
    ):

        db_product = product_repository.get_by_id(
            db,
            product_id,
        )

        if not db_product:
            raise ValueError("Product not found.")

        return product_repository.update(
            db,
            db_product,
            product,
        )

    def delete_product(
        self,
        db: Session,
        product_id: int,
    ):

        db_product = product_repository.get_by_id(
            db,
            product_id,
        )

        if not db_product:
            raise ValueError("Product not found.")

        product_repository.delete(
            db,
            db_product,
        )


product_service = ProductService()