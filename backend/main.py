from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from .models import mongo_ops


app = FastAPI(title="EComSight")

# Pydantic models for request validation
class ProductIn(BaseModel):
    name: str
    description: str = ""
    price: float
    category: str = ""
    attributes: Dict[str, Any] = {}

class OrderItem(BaseModel):
    product_id: str
    qty: int

class OrderIn(BaseModel):
    user_id: str
    items: List[OrderItem]
    total: float


@app.post("/products", summary="Create product")
def create_product(payload: ProductIn):
    try:
        data = payload.model_dump()
        prod_id = mongo_ops.add_product(data)
        return {"message": "product_created", "product_id": prod_id}
    
    except Exception:
        return {"message": "failed_product_creation"}
    

@app.get("/products", summary="Get all products")
def get_all_products_id():
    try:
        products = mongo_ops.get_all_products()
        return {"count": len(products), "products": products}
    except Exception as e:
        return {"error": str(e)}
    
