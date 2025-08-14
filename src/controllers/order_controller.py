import sys, os
from commands.write_order import WriteOrder
from flask import jsonify

class OrderController:

    def create_order(request):
        payload = request.get_json() or {}
        user_id = payload.get('user_id')
        items = payload.get('items', [])
        if not user_id or not items:
            return jsonify({'error':'user_id and items are required'}), 400
        try:
            print(user_id, items)
            order_id = WriteOrder.add_order(user_id, items)
            return jsonify({'order_id': order_id}), 201
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({'error': str(e)}), 500

    def delete_order(order_id):
        try:
            deleted = WriteOrder.remove_order(order_id)
            if deleted:
                return jsonify({'deleted': True})
            return jsonify({'deleted': False}), 404
        except Exception:
            return jsonify({'error': str(e)}), 500

    def get_order(order_id):
        return None