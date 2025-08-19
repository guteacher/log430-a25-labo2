"""
Orders (write-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
from sqlalchemy import text
from models.order import Order
from models.product import Product
from models.order_item import OrderItem
from db import get_sqlalchemy_session, get_redis_conn

def insert_order(user_id: int, items: list):
    """Insert order with items in MySQL, keep Redis in sync"""
    if not items:
        raise ValueError("Cannot create order. An order must have 1 or more items.")

    product_ids = [item['product_id'] for item in items]
    session = get_sqlalchemy_session()

    try:
        products_query = session.query(Product).filter(Product.id.in_(product_ids)).all()
        price_map = {product.id: product.price for product in products_query}
        
        total_amount = 0
        order_items_data = []
        
        for item in items:
            pid = item["product_id"]
            qty = item["quantity"]

            if pid not in price_map:
                raise ValueError(f"Product ID {pid} not found in database.")

            unit_price = price_map[pid]
            total_amount += unit_price * qty

            order_items_data.append({
                'product_id': pid,
                'quantity': qty,
                'unit_price': unit_price
            })

        new_order = Order(user_id=user_id, total_amount=total_amount)
        session.add(new_order)
        session.flush() 
        
        order_id = new_order.id

        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order_id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price']
            )
            session.add(order_item)

        # Update stocks
        update_stocks(session, order_items_data)

        session.commit()

        # Insert order into Redis
        insert_order_to_redis(order_id, user_id, total_amount, items)
        return order_id

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def delete_order(order_id: int):
    """Delete order in MySQL, keep Redis in sync"""
    session = get_sqlalchemy_session()
    try:
        order = session.query(Order).filter(Order.id == order_id).first()
        
        if order:
            session.delete(order)
            session.commit()
            delete_order_from_redis(order_id)

            order_items_data = session.query(OrderItem).filter(OrderItem.order_id == order_id).first()
            update_stocks(session, order_items_data)

            return 1  
        else:
            return 0  
            
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_stocks(session, order_items_data):
    try:
        when_clauses = []
        params = {}
        product_ids = [str(item['product_id']) for item in order_items_data]
        product_ids_str = ",".join(product_ids)
        for i, item in enumerate(order_items_data):
            pid = item['product_id']
            qty = item['quantity']
            when_clauses.append(f"WHEN product_id = :pid_{i} THEN :qty_{i}")
            params[f'pid_{i}'] = pid
            params[f'qty_{i}'] = qty
        
        when_clause_str = " ".join(when_clauses)
        
        query = text(f"""
            UPDATE product_stocks 
            SET quantity = quantity - (CASE {when_clause_str} END),
            WHERE product_id IN ({product_ids_str})
            AND quantity >= (CASE {when_clause_str} END)
        """)
        print(query, params) 
        session.execute(query, params)
    except Exception as e:
        raise e

def insert_order_to_redis(order_id, user_id, total_amount, items):
    """Insert order to Redis"""
    r = get_redis_conn()
    r.hset(
        f"order:{order_id}",
        mapping={
            "user_id": user_id,
            "total_amount": float(total_amount),
            "items": json.dumps(items)
        }
    )

def delete_order_from_redis(order_id):
    """Delete order from Redis"""
    r = get_redis_conn()
    r.delete(f"order:{order_id}")

