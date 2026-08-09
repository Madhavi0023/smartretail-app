from sqlalchemy.orm import Session

from app.modules.inventory.repository import inventory_repository
from app.modules.inventory.schema import StockTransactionCreate
from app.modules.products.model import Product


class InventoryService:

    def stock_in(
        self,
        db: Session,
        transaction: StockTransactionCreate,
    ):
        product = (
            db.query(Product)
            .filter(Product.id == transaction.product_id)
            .first()
        )

        if not product:
            raise ValueError("Product not found.")

        product.current_stock += transaction.quantity

        db.commit()
        db.refresh(product)

        return inventory_repository.create(
            db,
            product.id,
            "STOCK_IN",
            transaction,
        )

    def stock_out(
        self,
        db: Session,
        transaction: StockTransactionCreate,
    ):
        product = (
            db.query(Product)
            .filter(Product.id == transaction.product_id)
            .first()
        )

        if not product:
            raise ValueError("Product not found.")

        if product.current_stock < transaction.quantity:
            raise ValueError("Insufficient stock.")

        product.current_stock -= transaction.quantity

        db.commit()
        db.refresh(product)

        return inventory_repository.create(
            db,
            product.id,
            "STOCK_OUT",
            transaction,
        )

    def get_stock_history(
        self,
        db: Session,
        product_id: int,
    ):
        product = (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if not product:
            raise ValueError("Product not found.")

        return inventory_repository.get_by_product(
            db,
            product_id,
        )


inventory_service = InventoryService()