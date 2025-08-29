"""
User controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from flask import jsonify
from commands.write_user import insert_user, delete_user
from queries.read_user import get_user_by_id

def create_user(name, email):
    """Create user, use WriteUser model"""
    try:
        user_id = insert_user(name, email)
        return jsonify({'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def remove_user(user_id):
    """Delete user, use WriteUser model"""
    try:
        deleted = delete_user(user_id)
        if deleted:
            return jsonify({'deleted': True})
        return jsonify({'deleted': False}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_user(user_id):
    """Get user by id, use ReadUser model"""
    try:
        user = get_user_by_id(user_id)
        return jsonify(user), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500