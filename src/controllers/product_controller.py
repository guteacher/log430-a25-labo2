"""
Product controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from flask import jsonify
from commands.write_product import insert_product, delete_product
from queries.read_product import get_product_by_id

def create_product(name, sku, price):
    """Create product, use WriteProduct model"""
    try:
        product_id = insert_product(name, sku, price)
        return jsonify({'product_id': product_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def remove_product(product_id):
    """Delete product, use WriteProduct model"""
    try:
        deleted = delete_product(product_id)
        if deleted:
            return jsonify({'deleted': True})
        return jsonify({'deleted': False}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_product(product_id):
    """Get product by id, use ReadProduct model"""
    try:
        product = get_product_by_id(product_id)
        return jsonify(product), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500