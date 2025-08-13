from commands import write_order
from queries import read_order
from flask import jsonify

def create_order(request):
    payload = request.get_json() or {}
    user_id = payload.get('user_id')
    items = payload.get('items', [])
    if not user_id or not items:
        return jsonify({'error':'user_id and items are required'}), 400
    try:
        order_id = write_order.add_order(int(user_id), items)
        return jsonify({'order_id': order_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_order(order_id):
    try:
        deleted = write_order.remove_order(order_id)
        if deleted:
            return jsonify({'deleted': True})
        return jsonify({'deleted': False}), 404
    except Exception:
        return jsonify({'error': str(e)}), 500

def get_order(order_id):
    return None