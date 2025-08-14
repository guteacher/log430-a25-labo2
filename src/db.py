import mysql.connector
from mysql.connector import Error
import redis
import json
import config

def get_mysql_conn():
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME
    )

def get_redis_conn():
    return redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)

# Helper to cache query results in redis (simple serializer)
def cache_set(redis_conn, key, value):
    redis_conn.set(key, json.dumps(value))

def cache_get(redis_conn, key):
    v = redis_conn.get(key)
    return json.loads(v) if v else None
