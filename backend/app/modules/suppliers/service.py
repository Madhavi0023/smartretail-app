from sqlalchemy.orm import Session

from app.modules.suppliers.repository import supplier_repository
from app.modules.suppliers.schema import (
    SupplierCreate,
    SupplierUpdate,
)


class SupplierService:

    def create_supplier(
        self,
        db: Session,
        supplier: SupplierCreate,
    ):

        if not supplier.name.strip():
            raise ValueError("Supplier name is required.")

        return supplier_repository.create(
            db,
            supplier,
        )

    def get_all_suppliers(
        self,
        db: Session,
    ):
        return supplier_repository.get_all(db)

    def get_supplier_by_id(
        self,
        db: Session,
        supplier_id: int,
    ):

        supplier = supplier_repository.get_by_id(
            db,
            supplier_id,
        )

        if not supplier:
            raise ValueError("Supplier not found.")

        return supplier

    def update_supplier(
        self,
        db: Session,
        supplier_id: int,
        supplier: SupplierUpdate,
    ):

        db_supplier = supplier_repository.get_by_id(
            db,
            supplier_id,
        )

        if not db_supplier:
            raise ValueError("Supplier not found.")

        if supplier.name is not None and not supplier.name.strip():
            raise ValueError("Supplier name cannot be empty.")

        return supplier_repository.update(
            db,
            db_supplier,
            supplier,
        )

    def delete_supplier(
        self,
        db: Session,
        supplier_id: int,
    ):

        db_supplier = supplier_repository.get_by_id(
            db,
            supplier_id,
        )

        if not db_supplier:
            raise ValueError("Supplier not found.")

        supplier_repository.delete(
            db,
            db_supplier,
        )


supplier_service = SupplierService()