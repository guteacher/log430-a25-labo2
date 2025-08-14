from db import get_mysql_conn, get_redis_conn, cache_set
import sys, os
from decimal import Decimal
import json

class WriteOrder:
    
    def add_order(user_id: int, items: list):
        """
        Add an order for a user with multiple items.
        items format: [{'product_id': 1, 'quantity': 2}, ...]
        """

        if not items:
            raise ValueError("Items list cannot be empty.")

        product_ids = [item['product_id'] for item in items]

        # Get connection
        conn = get_mysql_conn()
        cursor = conn.cursor(dictionary=True) 

        try:
            # Get products
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

            # Insert orders
            cursor.execute(
                "INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)",
                (user_id, total_amount)
            )
            order_id = cursor.lastrowid

            # Insert order_items 
            values_placeholder = ", ".join(["(%s, %s, %s, %s)"] * len(order_items_data))
            values_data = []
            for pid, qty, price in order_items_data:
                values_data.extend([order_id, pid, qty, price])

            cursor.execute(
                f"INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES {values_placeholder}",
                values_data
            )
            conn.commit()

            # update Redis
            WriteOrder.update_orders_on_redis(order_id, user_id, items)

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

            # TODO: remove orders from redis
            r = get_redis_conn()
            existing_orders = r.get('orders')
            if existing_orders:
                pass

            return cur.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def update_orders_on_redis(order_id, user_id, items):
        r = get_redis_conn()
        existing_orders = r.get('orders')
        order_obj = {"order_id": order_id, "user_id": user_id, "items": items}
        if existing_orders == {}:
            orders_string = json.dumps([order_obj], separators=(',', ':'))
        else:
            existing_orders_list = json.loads(existing_orders)
            print(existing_orders_list)
            orders_string = json.dumps([order_obj] + existing_orders_list, separators=(',', ':'))
        r.set('orders', orders_string)


