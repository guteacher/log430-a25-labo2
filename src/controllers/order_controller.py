"""
Order controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from flask import jsonify
from commands.write_order import add_order, remove_order
from queries.read_order import get_order_by_id

def create_order(request):
    payload = request.get_json() or {}
    user_id = payload.get('user_id')
    items = payload.get('items', [])
    if not user_id or not items:
        return jsonify({'error':'user_id and items are required'}), 400
    try:
        order_id = add_order(user_id, items)
        return jsonify({'order_id': order_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_order(order_id):
    try:
        deleted = remove_order(order_id)
        if deleted:
            return jsonify({'deleted': True})
        return jsonify({'deleted': False}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_order(order_id):
    try:
        order = get_order_by_id(order_id)
        return jsonify(order), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500