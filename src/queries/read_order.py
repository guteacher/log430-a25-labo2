from db import get_redis_conn, get_mysql_conn, cache_set, cache_get

class ReadOrder:
    # TODO: read from redis ONLY
    def get_best_selling_products():
        return []

    # TODO: read from redis ONLY
    def get_highest_spending_users():
        return []
