
from sqlalchemy.orm import Session

from app.modules.products.model import Product
from app.modules.products.schema import ProductCreate, ProductUpdate


class ProductRepository:

    def create(self, db: Session, product: ProductCreate) -> Product:
        print("Repository create() called")
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def get_all(self, db: Session):
        return db.query(Product).all()

    def get_by_id(self, db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    def get_by_sku(self, db: Session, sku: str):
        return db.query(Product).filter(Product.sku == sku).first()

    def update(
        self,
        db: Session,
        db_product: Product,
        product: ProductUpdate,
    ):
        update_data = product.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)

        return db_product

    def delete(self, db: Session, db_product: Product):
        db.delete(db_product)
        db.commit()


product_repository = ProductRepository()