"""
Order manager application
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from flask import Flask, request, jsonify
from queries.read_order import get_best_selling_products, get_highest_spending_users
from controllers.order_controller import create_order, delete_order
from controllers.product_controller import create_product
from controllers.user_controller import create_user
app = Flask(__name__)

@app.get('/health')
def health():
    """Return OK if app is up and running"""
    return jsonify({'status':'ok'})

# Write routes (Commands)
@app.post('/orders')
def post_orders():
    """Create a new order based on information on request body"""
    return create_order(request)

@app.post('/products')
def products():
    """Get order with a given xxxx"""
    return create_product(request)

@app.post('/users')
def users():
    """Get order with a given xxxxx"""
    return create_user(request)

@app.delete('/orders/<int:order_id>')
def delete_orders_id(order_id):
    """Delete an order with a given order_id"""
    return delete_order(order_id)

# Read routes (Queries) 
@app.get('/orders/<int:order_id>')
def get_order(order_id):
    """Get order with a given order_id"""
    return get_order(order_id)

@app.get('/orders/reports/highest_spenders')
def get_users_ranked():
    """Get list of highest speding users, order by total expenditure"""
    rows = get_highest_spending_users()
    return jsonify(rows)

@app.get('/orders/reports/best_sellers')
def get_best_selling_products():
    """Get list of best selling products, order by number of orders"""
    rows = get_best_selling_products()
    return jsonify(rows)

# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
