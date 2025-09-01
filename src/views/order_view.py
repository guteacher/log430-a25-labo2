"""
Order view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import numbers
from views.template_view import get_template, get_param
from controllers.order_controller import create_order, delete_order, list_orders
from controllers.product_controller import list_products
from controllers.user_controller import list_users

def show_order_form():
    """ Show order form and list """
    orders = list_orders(10)
    products = list_products(99)
    users = list_users(99)
    return get_template(f"""
        <h2>Commandes</h2>
        <p>Les 10 derniers enregistrements</p>
        <ul>
            {" ".join([f"""<li><a href="/orders/remove/{order.id}">[x]</a> Commande {order.id}, ${order.total_amount}  </li>""" for order in orders])}
        </ul>
        <h2>Enregistrement</h2>
        <form method="POST" action="/orders/add">
           <label>Utilisateur <select name="user_id" required>
                {" ".join([f"""<option key={user.id} value={user.id}>{user.name}</option>""" for user in users])}
           </select></label><br>
           <label>Article <select name="product_id" required>
                {" ".join([f"""<option key={product.id} value={product.id}>{product.name} (${product.price})</option>""" for product in products])}
           </select></label><br>
           <label>Quantité <input type="number" name="quantity" step="1" value="1" min="1" max="999" required></label><br>
           <input type="submit" value="Enregistrer">
        </form>
    """)

def register_order(params):
    """ Add an order based on given params """
    if len(params.keys()):
        user_id = get_param(params, "user_id")
        product_id = get_param(params, "product_id")
        quantity = get_param(params, "quantity")
        items = [
            {'product_id': product_id, 'quantity': quantity}
        ]
        result = create_order(user_id, items)
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
    """ Remove an order with the given ID """
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