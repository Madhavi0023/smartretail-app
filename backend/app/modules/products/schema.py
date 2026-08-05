from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    sku: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    category: str
    brand: str

    purchase_price: Decimal = Field(..., gt=0)
    selling_price: Decimal = Field(..., gt=0)

    current_stock: int = Field(..., ge=0)
    minimum_stock: int = Field(..., ge=0)

    unit: str = "Piece"
    barcode: Optional[str] = None
    status: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None

    purchase_price: Optional[Decimal] = Field(None, gt=0)
    selling_price: Optional[Decimal] = Field(None, gt=0)

    current_stock: Optional[int] = Field(None, ge=0)
    minimum_stock: Optional[int] = Field(None, ge=0)

    unit: Optional[str] = None
    barcode: Optional[str] = None
    status: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)