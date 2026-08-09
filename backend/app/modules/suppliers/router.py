from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.suppliers.schema import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)
from app.modules.suppliers.service import supplier_service


router = APIRouter(
    prefix="/api/v1/suppliers",
    tags=["Suppliers"],
)


@router.post(
    "/",
    response_model=SupplierResponse,
    status_code=201,
)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
):
    try:
        return supplier_service.create_supplier(
            db,
            supplier,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=List[SupplierResponse],
)
def get_suppliers(
    db: Session = Depends(get_db),
):
    return supplier_service.get_all_suppliers(db)


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse,
)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    try:
        return supplier_service.get_supplier_by_id(
            db,
            supplier_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse,
)
def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db),
):
    try:
        return supplier_service.update_supplier(
            db,
            supplier_id,
            supplier,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete(
    "/{supplier_id}",
)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    try:
        supplier_service.delete_supplier(
            db,
            supplier_id,
        )

        return {
            "message": "Supplier deleted successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )