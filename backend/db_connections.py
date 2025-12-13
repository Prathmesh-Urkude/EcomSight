import time
import sys
from pymongo import MongoClient
import redis
from cassandra.cluster import Cluster

# Config
MONGO_URI = "mongodb://localhost:27017"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
CASSANDRA_CONTACT_POINTS = ["127.0.0.1"]  # Cassandra container mapped to localhost:9042

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

# Cassandra
def get_cassandra_session():
    for attempt in range(RETRY_MAX):
        try:
            cluster = Cluster(CASSANDRA_CONTACT_POINTS)
            session = cluster.connect()

            # create keyspace and table if not exists
            session.execute("""
            CREATE KEYSPACE IF NOT EXISTS ecom
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
            """)

            session.set_keyspace('ecom')

            session.execute("""
            CREATE TABLE IF NOT EXISTS user_events (
                product_id text,
                event_date date,
                event_time timestamp,
                user_id text,
                session_id text,
                event_type text,
                event_props map<text, text>,
                PRIMARY KEY ((product_id, event_date), event_time, user_id)
            ) WITH CLUSTERING ORDER BY (event_time DESC)
            """)

            # validate by simple query
            session.execute("SELECT now() FROM system.local")
        
            print("Connected to Cassandra")
            return session
        
        except Exception as e:
            print(f"Cassandra connect attempt {attempt+1}/{RETRY_MAX} failed: {e}")
            time.sleep(RETRY_DELAY)

    print("Could not connect to Cassandra. Exiting.")
    sys.exit(1)

cassandra_session = get_cassandra_session()