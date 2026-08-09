from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.inventory.schema import (
    StockTransactionCreate,
    StockTransactionResponse,
)
from app.modules.inventory.service import inventory_service


router = APIRouter(
    prefix="/api/v1/inventory",
    tags=["Inventory"],
)


@router.post(
    "/stock-in",
    response_model=StockTransactionResponse,
    status_code=201,
)
def stock_in(
    transaction: StockTransactionCreate,
    db: Session = Depends(get_db),
):
    try:
        return inventory_service.stock_in(
            db,
            transaction,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post(
    "/stock-out",
    response_model=StockTransactionResponse,
    status_code=201,
)
def stock_out(
    transaction: StockTransactionCreate,
    db: Session = Depends(get_db),
):
    try:
        return inventory_service.stock_out(
            db,
            transaction,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/history/{product_id}",
    response_model=List[StockTransactionResponse],
)
def get_stock_history(
    product_id: int,
    db: Session = Depends(get_db),
):
    try:
        return inventory_service.get_stock_history(
            db,
            product_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )