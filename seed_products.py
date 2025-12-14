from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client.ecom_db

products = [
    {"name": "Noise-cancelling Headphones", "description": "Immersive sound", "price": 129.99, "category": "audio", "attributes": {"battery": "30h"}},
    {"name": "Mechanical Keyboard", "description": "Tactile keys", "price": 79.99, "category": "peripherals", "attributes": {"switch": "blue"}},
    {"name": "Smart Watch", "description": "Health & notifications", "price": 199.99, "category": "wearables", "attributes": {"waterproof": True}},
    {"name": "4K Monitor", "description": "Ultra HD display", "price": 349.99, "category": "display", "attributes": {"size": "27-inch"}},
    {"name": "Wireless Mouse", "description": "Ergonomic design", "price": 39.99, "category": "peripherals", "attributes": {"dpi": 16000}},
    {"name": "Bluetooth Speaker", "description": "Portable and powerful", "price": 59.99, "category": "audio", "attributes": {"battery": "12h"}},
    {"name": "Gaming Laptop", "description": "High performance for gamers", "price": 1499.99, "category": "computers", "attributes": {"gpu": "RTX 4070"}},
    {"name": "External SSD", "description": "Fast data transfer", "price": 119.99, "category": "storage", "attributes": {"capacity": "1TB"}},
    {"name": "Smartphone Gimbal", "description": "Stabilized video capture", "price": 89.99, "category": "accessories", "attributes": {"axis": "3-axis"}},
    {"name": "VR Headset", "description": "Immersive virtual experience", "price": 299.99, "category": "gaming", "attributes": {"resolution": "2160x1200"}},
    {"name": "Action Camera", "description": "Capture adventures", "price": 249.99, "category": "cameras", "attributes": {"waterproof": True}},
    {"name": "Smart Light Bulb", "description": "Color-changing LED", "price": 24.99, "category": "smart home", "attributes": {"connectivity": "Wi-Fi"}},
    {"name": "Portable Projector", "description": "Compact HD projection", "price": 229.99, "category": "entertainment", "attributes": {"brightness": "600 ANSI lumens"}}

]

res = db.products.insert_many(products)
print("Inserted products:", [str(x) for x in res.inserted_ids])
