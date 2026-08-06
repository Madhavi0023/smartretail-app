from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.products.schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.modules.products.service import product_service



router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
)


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    try:
        return product_service.create_product(db, product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ProductResponse])
def get_products(
    db: Session = Depends(get_db),
):
    return product_service.get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    try:
        return product_service.get_product_by_id(
            db,
            product_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    try:
        return product_service.update_product(
            db,
            product_id,
            product,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    try:
        product_service.delete_product(
            db,
            product_id,
        )
        return {
            "message": "Product deleted successfully."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))