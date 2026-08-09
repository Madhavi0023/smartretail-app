from sqlalchemy.orm import Session

from app.modules.suppliers.model import Supplier
from app.modules.suppliers.schema import SupplierCreate, SupplierUpdate


class SupplierRepository:

    def create(
        self,
        db: Session,
        supplier: SupplierCreate,
    ) -> Supplier:

        db_supplier = Supplier(
            **supplier.model_dump()
        )

        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)

        return db_supplier

    def get_all(self, db: Session):
        return db.query(Supplier).all()

    def get_by_id(
        self,
        db: Session,
        supplier_id: int,
    ):
        return (
            db.query(Supplier)
            .filter(Supplier.id == supplier_id)
            .first()
        )

    def update(
        self,
        db: Session,
        db_supplier: Supplier,
        supplier: SupplierUpdate,
    ):

        update_data = supplier.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(db_supplier, key, value)

        db.commit()
        db.refresh(db_supplier)

        return db_supplier

    def delete(
        self,
        db: Session,
        db_supplier: Supplier,
    ):

        db.delete(db_supplier)
        db.commit()


supplier_repository = SupplierRepository()