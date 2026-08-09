from sqlalchemy.orm import Session

from app.modules.inventory.model import StockTransaction
from app.modules.inventory.schema import StockTransactionCreate


class InventoryRepository:

    def create(
        self,
        db: Session,
        product_id: int,
        transaction_type: str,
        transaction: StockTransactionCreate,
    ) -> StockTransaction:

        db_transaction = StockTransaction(
            product_id=product_id,
            transaction_type=transaction_type,
            quantity=transaction.quantity,
            remarks=transaction.remarks,
        )

        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        return db_transaction

    def get_by_product(
        self,
        db: Session,
        product_id: int,
    ):
        return (
            db.query(StockTransaction)
            .filter(StockTransaction.product_id == product_id)
            .order_by(StockTransaction.created_at.desc())
            .all()
        )


inventory_repository = InventoryRepository()