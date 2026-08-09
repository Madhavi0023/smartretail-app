from sqlalchemy.orm import Session

from app.modules.inventory.model import StockTransaction
from app.modules.purchase.model import Purchase, PurchaseItem
from app.modules.purchase.repository import purchase_repository
from app.modules.purchase.schema import PurchaseCreate
from app.modules.products.model import Product
from app.modules.suppliers.model import Supplier


class PurchaseService:
    def create_purchase(
        self,
        db: Session,
        purchase_data: PurchaseCreate,
    ):
        supplier = (
            db.query(Supplier)
            .filter(
                Supplier.id == purchase_data.supplier_id
            )
            .first()
        )

        if not supplier:
            raise ValueError("Supplier not found.")

        if purchase_data.invoice_number:
            existing_purchase = (
                db.query(Purchase)
                .filter(
                    Purchase.invoice_number
                    == purchase_data.invoice_number
                )
                .first()
            )

            if existing_purchase:
                raise ValueError(
                    "Purchase with this invoice number already exists."
                )

        if not purchase_data.items:
            raise ValueError(
                "Purchase must contain at least one item."
            )

        purchase = Purchase(
            supplier_id=purchase_data.supplier_id,
            invoice_number=purchase_data.invoice_number,
            total_amount=0,
        )

        db.add(purchase)
        db.flush()

        total_amount = 0

        for item_data in purchase_data.items:
            product = (
                db.query(Product)
                .filter(
                    Product.id == item_data.product_id
                )
                .first()
            )

            if not product:
                raise ValueError(
                    f"Product {item_data.product_id} not found."
                )

            subtotal = (
                item_data.quantity
                * item_data.purchase_price
            )

            purchase_item = PurchaseItem(
                purchase_id=purchase.id,
                product_id=product.id,
                quantity=item_data.quantity,
                purchase_price=item_data.purchase_price,
                subtotal=subtotal,
            )

            db.add(purchase_item)

            product.current_stock += item_data.quantity

            stock_transaction = StockTransaction(
                product_id=product.id,
                transaction_type="STOCK_IN",
                quantity=item_data.quantity,
                remarks=f"Purchase #{purchase.id}",
            )

            db.add(stock_transaction)

            total_amount += subtotal

        purchase.total_amount = total_amount

        db.commit()
        db.refresh(purchase)

        return purchase

    def get_all_purchases(
        self,
        db: Session,
    ):
        return purchase_repository.get_all(db)

    def get_purchase_by_id(
        self,
        db: Session,
        purchase_id: int,
    ):
        purchase = purchase_repository.get_by_id(
            db,
            purchase_id,
        )

        if not purchase:
            raise ValueError("Purchase not found.")

        return purchase


purchase_service = PurchaseService()