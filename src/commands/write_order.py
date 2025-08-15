"""
Orders (write-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
from db import get_mysql_conn, get_redis_conn

def add_order(user_id: int, items: list):
    if not items:
        raise ValueError("Cannot create order. An order must have 1 or more items.")

    product_ids = [item['product_id'] for item in items]

    # démarrer une connexion MySQL
    conn = get_mysql_conn()
    cursor = conn.cursor(dictionary=True) 

    try:
        # sélectionner : products
        placeholders = ", ".join(["%s"] * len(product_ids))
        cursor.execute(
            f"SELECT id, price FROM products WHERE id IN ({placeholders})",
            product_ids
        )
        products_data = cursor.fetchall()
        price_map = {row["id"]: row["price"] for row in products_data}
        total_amount = 0
        order_items_data = []
        for item in items:
            pid = item["product_id"]
            qty = item["quantity"]

            if pid not in price_map:
                raise ValueError(f"Product ID {pid} not found in database.")

            unit_price = price_map[pid]
            total_amount += unit_price * qty

            order_items_data.append((pid, qty, unit_price))

        # insérer : order
        cursor.execute(
            "INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)",
            (user_id, total_amount)
        )
        order_id = cursor.lastrowid

        # insérer : order_item (MySQL)
        values_placeholder = ", ".join(["(%s, %s, %s, %s)"] * len(order_items_data))
        values_data = []
        for pid, qty, price in order_items_data:
            values_data.extend([order_id, pid, qty, price])

        cursor.execute(
            f"INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES {values_placeholder}",
            values_data
        )
        conn.commit()

        # insérer : order (Redis)
        add_order_to_redis(order_id, user_id, total_amount, items)

        return cursor.lastrowid

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def remove_order(order_id: int):
    conn = get_mysql_conn()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM orders WHERE id=%s", (order_id,))
        conn.commit()
         # supprimer : order (Redis)
        remove_order_from_redis(order_id)
        return cur.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def add_order_to_redis(order_id, user_id, total_amount, items):
    r = get_redis_conn()
    r.hset(
        f"order:{order_id}",
        mapping={
            "user_id": user_id,
            "total_amount": float(total_amount),
            "items": json.dumps(items)
        }
    )

def remove_order_from_redis(order_id):
    r = get_redis_conn()
    r.delete(f"order:{order_id}")

