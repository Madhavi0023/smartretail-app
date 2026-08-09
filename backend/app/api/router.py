from fastapi import APIRouter

from app.api.health import router as health_router
from app.modules.products.router import router as product_router
from app.modules.inventory.router import router as inventory_router
from app.modules.suppliers.router import router as supplier_router
from app.modules.purchase.router import router as purchase_router


api_router = APIRouter()


api_router.include_router(health_router)
api_router.include_router(product_router)
api_router.include_router(inventory_router)
api_router.include_router(supplier_router)
api_router.include_router(purchase_router)