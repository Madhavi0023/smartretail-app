from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.purchase.schema import (
    PurchaseCreate,
    PurchaseResponse,
)
from app.modules.purchase.service import purchase_service


router = APIRouter(
    prefix="/api/v1/purchases",
    tags=["Purchases"],
)


@router.post(
    "/",
    response_model=PurchaseResponse,
    status_code=201,
)
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
):
    try:
        return purchase_service.create_purchase(
            db,
            purchase,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=List[PurchaseResponse],
)
def get_purchases(
    db: Session = Depends(get_db),
):
    return purchase_service.get_all_purchases(db)


@router.get(
    "/{purchase_id}",
    response_model=PurchaseResponse,
)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
):
    try:
        return purchase_service.get_purchase_by_id(
            db,
            purchase_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )