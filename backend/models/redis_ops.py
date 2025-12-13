import json
from ..db_connections import redis_client

def cache_product(product_id: str, product_data: dict, ttl: int = 1800):
    key = f"product:cache:{product_id}"
    redis_client.setex(key, ttl, json.dumps(product_data, default=str))

def get_cached_product(product_id: str):
    key = f"product:cache:{product_id}"
    raw = redis_client.get(key)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None

def increment_product_view(product_id: str) -> int:
    key = f"counter:product:views:{product_id}"
    redis_client.incr(key)
    # return updated count
    val = redis_client.get(key)
    return int(val or 0)

def add_to_leaderboard(product_id: str, score: int = 1):
    key = "leaderboard:top_products"
    redis_client.zincrby(key, score, product_id)

def get_top_products(n: int = 10):
    key = "leaderboard:top_products"
    # ZREVRANGE with scores
    items = redis_client.zrevrange(key, 0, n-1, withscores=True)
    return items
