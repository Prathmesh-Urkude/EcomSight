import time
import sys
from pymongo import MongoClient
import redis

# Config
MONGO_URI = "mongodb://localhost:27017"
REDIS_HOST = "localhost"
REDIS_PORT = 6379

RETRY_MAX = 20
RETRY_DELAY = 2  # seconds

# MongoDB
def get_mongo_client():
    for attempt in range(RETRY_MAX):
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
            # trigger server selection
            client.admin.command('ping')
            print("Connected to MongoDB")
            return client
        
        except Exception as e:
            print(f"Mongo connect attempt {attempt+1}/{RETRY_MAX} failed: {e}")
            time.sleep(RETRY_DELAY)

    print("Could not connect to MongoDB. Exiting.")
    sys.exit(1)

mongo_client = get_mongo_client()
mongo_db = mongo_client["ecom_db"]

# Redis
def get_redis_client():
    for attempt in range(RETRY_MAX):
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            r.ping()
            print("Connected to Redis")
            return r
        
        except Exception as e:
            print(f"Redis connect attempt {attempt+1}/{RETRY_MAX} failed: {e}")
            time.sleep(RETRY_DELAY)

    print("Could not connect to Redis. Exiting.")
    sys.exit(1)

redis_client = get_redis_client()

