from fastapi import FastAPI, Request, HTTPException
from bson import ObjectId
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from .models import mongo_ops, redis_ops, cassandra_ops


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
    

@app.get("/products/{product_id}", summary="Get product (cache + event logging)")
def get_product(product_id: str, request: Request):
    user_id = request.headers.get("X-User-Id", "guest")
    session_id = request.headers.get("X-Session-Id", f"session_{user_id}")

    # Try cache
    cached = redis_ops.get_cached_product(product_id)
    if cached:
        product = cached
    else:
        product = mongo_ops.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Convert ObjectId to str for JSON serialization before caching
        if "_id" in product and isinstance(product["_id"], ObjectId):
            product["_id"] = str(product["_id"])

        redis_ops.cache_product(product_id, product, ttl=1800)

    # increment counters & leaderboard
    redis_ops.increment_product_view(product_id)
    redis_ops.add_to_leaderboard(product_id, 1)

    # log event to cassandra
    cassandra_ops.log_event(product_id, user_id, session_id, "view", {"source": "product_api"})

    return product

@app.post("/orders", summary="Place an order")
def place_order(order: OrderIn, request: Request):
    user_id = order.user_id
    session_id = request.headers.get("X-Session-Id", f"session_{user_id}")
    order_doc = {
        "user_id": order.user_id,
        "items": [item.model_dump() for item in order.items],
        "total": order.total
    }
    order_id = mongo_ops.create_order(order_doc)

    # Log purchase events for each item
    for it in order.items:
        cassandra_ops.log_event(it.product_id, user_id, session_id, "purchase", {"order_id": order_id, "qty": it.qty})

    return {"message": "order_placed", "order_id": order_id}