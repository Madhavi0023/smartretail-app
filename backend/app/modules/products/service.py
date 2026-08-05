from app.modules.products.schema import ProductCreate, ProductUpdate


class ProductService:

    def create_product(self, product: ProductCreate):
        return {
            "id": 1,
            **product.model_dump()
        }

    def get_products(self):
        return []

    def get_product(self, product_id: int):
        return {
            "id": product_id,
            "sku": "SKU-1001",
            "name": "Wireless Mouse",
            "description": "Demo Product",
            "category": "Electronics",
            "brand": "Logitech",
            "purchase_price": 500,
            "selling_price": 799,
            "current_stock": 100,
            "minimum_stock": 10,
            "unit": "Piece",
            "barcode": "8901234567890",
            "status": True,
        }

    def update_product(self, product_id: int, product: ProductUpdate):
        return {
            "id": product_id,
            "sku": "SKU-1001",
            "name": product.name or "Wireless Mouse",
            "description": product.description,
            "category": product.category or "Electronics",
            "brand": product.brand or "Logitech",
            "purchase_price": product.purchase_price or 500,
            "selling_price": product.selling_price or 799,
            "current_stock": product.current_stock or 100,
            "minimum_stock": product.minimum_stock or 10,
            "unit": product.unit or "Piece",
            "barcode": product.barcode,
            "status": True if product.status is None else product.status,
        }

    def delete_product(self, product_id: int):
        return {
            "message": f"Product {product_id} deleted successfully."
        }


product_service = ProductService()