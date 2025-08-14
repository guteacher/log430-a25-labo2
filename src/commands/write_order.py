from db import get_mysql_conn, get_redis_conn, cache_set
import sys, os
from decimal import Decimal

class WriteOrder:
    
    def add_order(user_id: int, items: list):
        """
        Add an order for a user with multiple items.
        items format: [{'product_id': 1, 'quantity': 2}, ...]
        """

        if not items:
            raise ValueError("Items list cannot be empty.")

        # Extract product IDs
        product_ids = [item['product_id'] for item in items]

        # Connect to the database
        conn = get_mysql_conn()
        cursor = conn.cursor(dictionary=True)  # dictionary=True so we get column names

        try:
            # Fetch all product prices at once
            placeholders = ", ".join(["%s"] * len(product_ids))
            cursor.execute(
                f"SELECT id, price FROM products WHERE id IN ({placeholders})",
                product_ids
            )
            products_data = cursor.fetchall()

            # Map product_id → price
            price_map = {row["id"]: row["price"] for row in products_data}

            # Compute total amount
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

            # Insert into orders table
            cursor.execute(
                "INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)",
                (user_id, total_amount)
            )
            order_id = cursor.lastrowid

            # Insert into order_items in one go
            values_placeholder = ", ".join(["(%s, %s, %s, %s)"] * len(order_items_data))
            values_data = []
            for pid, qty, price in order_items_data:
                values_data.extend([order_id, pid, qty, price])

            cursor.execute(
                f"INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES {values_placeholder}",
                values_data
            )

            # Commit transaction
            conn.commit()
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
            # delete order; foreign keys will remove items
            cur.execute("DELETE FROM orders WHERE id=%s", (order_id,))
            conn.commit()
            r = get_redis_conn()
            # invalidate caches that depend on orders
            # TODO: update cache, do not simply invalidate
            r.delete('best_selling_products')
            r.delete('highest_spending_users')
            return cur.rowcount
        finally:
            cur.close()
            conn.close()

    def update_best_selling_products():
        pass

    def update_highest_spending_users():
        pass

