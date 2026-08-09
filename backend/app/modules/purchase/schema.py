from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    purchase_price: Decimal = Field(gt=0)


class PurchaseCreate(BaseModel):
    supplier_id: int
    invoice_number: str | None = None
    items: list[PurchaseItemCreate]


class PurchaseItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    purchase_price: Decimal
    subtotal: Decimal

    model_config = {
        "from_attributes": True
    }


class PurchaseResponse(BaseModel):
    id: int
    supplier_id: int
    invoice_number: str | None
    total_amount: Decimal
    created_at: datetime
    items: list[PurchaseItemResponse]

    model_config = {
        "from_attributes": True
    }