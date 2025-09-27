"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from collections import defaultdict
import json
from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    r = get_redis_conn()
    order_keys = r.keys("order:*")
    return order_keys[0:limit]

def get_highest_spending_users():
    """Get report of highest spending users from Redis"""
    r = get_redis_conn()
    limit = 10
    result = []
    order_keys = r.keys("order:*")
    spending = defaultdict(float)
    
    for key in order_keys:
        order_data = r.hgetall(key)
        if "user_id" in order_data and "total_amount" in order_data:
            user_id = int(order_data["user_id"])
            total = float(order_data["total_amount"])
            spending[user_id] += total

    # Trier par total dépensé (décroissant), limite X
    highest_spending_users = sorted(spending.items(), key=lambda x: x[1], reverse=True)[:limit]
    for user in highest_spending_users:
        result.append({
            "user_id": user[0],
            "total_expense": round(user[1], 2)
        })

    return result

def get_best_selling_products():
    """Get report of best selling products by quantity sold from Redis"""
    r = get_redis_conn()
    limit = 10
    result = []
    order_keys = r.keys("order:*")
    product_sales = defaultdict(int)
    
    for order_key in order_keys:
        order_data = r.hgetall(order_key)
        if "items" in order_data:
            try:
                products = json.loads(order_data["items"])
            except Exception:
                continue

            for item in products:
                product_id = int(item.get("product_id", 0))
                quantity = int(item.get("quantity", 0))
                product_sales[product_id] += quantity

    # Trier par total vendu (décroissant), limite X
    best_selling = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:limit]
    for product in best_selling:
        result.append({
            "product_id": product[0],
            "quantity_sold": product[1]
        })

    return result
