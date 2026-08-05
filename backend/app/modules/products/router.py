from typing import List

from fastapi import APIRouter

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
def create_product(product: ProductCreate):
    """
    Create a new product.
    """
    return product_service.create_product(product)


@router.get("/", response_model=List[ProductResponse])
def get_products():
    """
    Get all products.
    """
    return product_service.get_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """
    Get product by ID.
    """
    return product_service.get_product(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate):
    """
    Update an existing product.
    """
    return product_service.update_product(product_id, product)


@router.delete("/{product_id}")
def delete_product(product_id: int):
    """
    Delete a product.
    """
    return product_service.delete_product(product_id)