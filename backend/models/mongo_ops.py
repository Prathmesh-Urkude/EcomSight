from datetime import datetime, timezone
from bson import ObjectId
from ..db_connections import mongo_db

products_collection = mongo_db.products
orders_collection = mongo_db.orders

def add_product(product_data: dict) -> str:
    product_data["created_at"] = datetime.now(timezone.utc)
    result = products_collection.insert_one(product_data)
    return str(result.inserted_id)

def get_product(product_id: str) -> dict:
    try:
        oid = ObjectId(product_id)
        doc = products_collection.find_one({"_id": oid})
        return doc

    except Exception:
        doc = products_collection.find_one({"_id": product_id})
        return doc
    

def get_all_products():
    try:
        products = products_collection.find({}, {"name": 1 ,"price": 1 ,"category": 1})       
    
        results = []
        for doc in products:
            pid = str(doc.get("_id"))
            results.append({
                "product_id": pid,
                "name": doc.get("name"),
                "price": doc.get("price"),
                "category": doc.get("category")
            })
        return results

    except Exception as e:
        print("Error fetching product IDs and names:", e)
        return []
    

def create_order(order_data: dict) -> str:
    order_data["created_at"] = datetime.now(timezone.utc)
    result = orders_collection.insert_one(order_data)
    return str(result.inserted_id)
