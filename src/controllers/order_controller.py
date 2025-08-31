"""
Order controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import numbers
from commands.write_order import insert_order, delete_order
from queries.read_order import get_orders

def create_order(user_id, items):
    """Create order, use WriteOrder model"""
    try:
        return insert_order(user_id, items)
    except ValueError as e:
        return str(e)
    except Exception as e:
        print(e)
        return "Une erreur s'est produite lors de la création de l'enregistrement. Veuillez consulter les logs pour plus d'informations."

def remove_order(order_id):
    """Delete order, use WriteOrder model"""
    try:
        return delete_order(order_id)
    except Exception as e:
        print(e)
        return "Une erreur s'est produite lors de la supression de l'enregistrement. Veuillez consulter les logs pour plus d'informations."

def list_orders(limit):
    """Get last X orders, use ReadOrder model"""
    try:
        return get_orders(limit)
    except Exception as e:
        print(e)
        return "Une erreur s'est produite lors de la requête de base de données. Veuillez consulter les logs pour plus d'informations."
    
def get_report_highest_spending_users():
    """Get orders report: highest spending users"""
    # TODO: appeler la méthode correspondante dans read_order.py
    return []

def get_report_best_selling_products():
    """Get orders report: best selling products"""
    # TODO: appeler la méthode correspondante dans read_order.py
    return []