"""
Order view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import numbers
from views.template_view import get_template, get_param
from controllers.order_controller import create_order, delete_order, list_orders

def show_order_form():
    orders = list_orders(10)
    return get_template(f"""
        <h2>Commandes</h2>
        <ul>
            {" ".join([f"""<li><a href="/orders/remove/{order.id}">[x]</a> {order.id} </li>""" for order in orders])}
        </ul>
        <h2>Enregistrement</h2>
        <form method="POST" action="/orders/add">
           <input type="submit" value="Enregistrer">
        </form>
    """)

def register_order(params):
    if len(params.keys()):
        name = get_param(params, "name")
        sku = get_param(params, "sku")
        price = get_param(params, "price")
        result = create_order(name, sku, price)
    else: 
        return get_template(f"""
                <h2>Erreur</h2>
                <code>La requête est vide</code>
            """)

    if isinstance(result, numbers.Number):
        return get_template(f"""
                <h2>Information: la commande {result} a été ajoutée.</h2>
                <a href="/orders">← Retourner à la page des commandes</a>
            """)
    else:
        return get_template(f"""
                <h2>Erreur</h2>
                <code>{result}</code>
            """)
    
def remove_order(order_id):
    result = delete_order(order_id)
    if result:
        return get_template(f"""
            <h2>Information: la commande {order_id} a été supprimée.</h2>
            <a href="/orders">← Retourner à la page des commandes</a>
        """)
    else:
        return get_template(f"""
                <h2>Erreur</h2>
                <code>{result}</code>
            """)