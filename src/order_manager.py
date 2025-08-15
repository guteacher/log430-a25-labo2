"""
Order manager application
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from flask import Flask, request, jsonify
from queries.read_order import get_best_selling_products, get_highest_spending_users
from controllers.order_controller import create_order, delete_order

app = Flask(__name__)

# observability routes
@app.get('/health')
def health():
    return jsonify({'status':'ok'})

# write routes (Commands)
@app.post('/orders')
def post_orders():
    return create_order(request)

@app.delete('/orders/<int:order_id>')
def delete_orders_id(order_id):
    return delete_order(order_id)

# read routes (Queries) 
@app.get('/orders/<int:order_id>')
def get_order(order_id):
    return get_order(order_id)

@app.get('/orders/reports/best_sellers')
def get_best_selling_products():
    rows = get_best_selling_products()
    return jsonify(rows)

@app.get('/orders/reports/highest_spenders')
def get_users_ranked():
    rows = get_highest_spending_users()
    return jsonify(rows)

# démarrer l'application Flask 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
