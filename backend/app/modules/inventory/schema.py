from datetime import datetime

from pydantic import BaseModel, Field


class StockTransactionCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    remarks: str | None = None


class StockTransactionResponse(BaseModel):
    id: int
    product_id: int
    transaction_type: str
    quantity: int
    remarks: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }