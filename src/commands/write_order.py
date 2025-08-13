from db import get_mysql_conn, get_redis_conn, cache_set
from decimal import Decimal

def add_order(user_id: int, items: list):
    '''
    items: list of dicts: [{'product_id': int, 'quantity': int}]
    This creates order, order_items and updates Redis caches for aggregates.
    '''
    conn = get_mysql_conn()
    cur = conn.cursor()
    try:
        # compute total from product prices
        total = Decimal('0.00')
        product_prices = {}
        # TODO: terrible code, fetch this once
        for it in items:
            cur.execute("SELECT price FROM products WHERE id=%s", (it['product_id'],))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Product {it['product_id']} not found")
            price = Decimal(str(row[0]))
            product_prices[it['product_id']] = price
            total += price * int(it.get('quantity',1))
        # insert order
        cur.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s,%s)", (user_id, float(total)))
        order_id = cur.lastrowid
        # insert items
        for it in items:
            pid = it['product_id']
            qty = int(it.get('quantity',1))
            cur.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s,%s,%s,%s)", (order_id, pid, qty, float(product_prices[pid])))
        conn.commit()
        # update Redis aggregates (best-effort; read side will be from redis)
        r = get_redis_conn()
        # invalidate caches that depend on orders
        # TODO: update cache, do not simply invalidate
        r.delete('best_selling_products')
        r.delete('highest_spending_users')
        return order_id
    finally:
        cur.close()
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

