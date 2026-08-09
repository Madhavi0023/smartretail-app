from datetime import datetime

from pydantic import BaseModel, EmailStr


class SupplierCreate(BaseModel):
    name: str
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    status: bool = True


class SupplierUpdate(BaseModel):
    name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    status: bool | None = None


class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_person: str | None
    phone: str | None
    email: str | None
    address: str | None
    status: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }