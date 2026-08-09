from sqlalchemy.orm import Session

from app.modules.purchase.model import Purchase, PurchaseItem


class PurchaseRepository:

    def create_purchase(
        self,
        db: Session,
        purchase: Purchase,
    ):

        db.add(purchase)
        db.commit()
        db.refresh(purchase)

        return purchase

    def get_all(
        self,
        db: Session,
    ):
        return db.query(Purchase).all()

    def get_by_id(
        self,
        db: Session,
        purchase_id: int,
    ):
        return (
            db.query(Purchase)
            .filter(Purchase.id == purchase_id)
            .first()
        )

    def add_item(
        self,
        db: Session,
        item: PurchaseItem,
    ):

        db.add(item)
        db.flush()

        return item

    def delete(
        self,
        db: Session,
        purchase: Purchase,
    ):

        db.delete(purchase)
        db.commit()


purchase_repository = PurchaseRepository()