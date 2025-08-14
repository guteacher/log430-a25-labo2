from flask import Flask, request, jsonify
from queries.read_order import ReadOrder
from controllers.order_controller import OrderController

app = Flask(__name__)

@app.get('/health')
def health():
    return jsonify({'status':'ok'})

# Write routes (commands)
@app.post('/orders')
def post_orders():
    return OrderController.create_order(request)

@app.delete('/orders/<int:order_id>')
def delete_orders_id(order_id):
    return OrderController.delete_order(order_id)

# Read routes (queries) 
@app.get('/orders/<int:order_id>')
def get_order(order_id):
    return OrderController.get_order(order_id)

@app.get('/orders/reports/best_sellers')
def get_best_selling_products():
    rows = ReadOrder.get_best_selling_products()
    return jsonify(rows)

@app.get('/orders/reports/highest_spenders')
def get_users_ranked():
    rows = ReadOrder.get_highest_spending_users()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
