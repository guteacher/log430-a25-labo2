"""
Product view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import numbers
from views.template_view import get_template, get_param
from controllers.product_controller import create_product, delete_product, list_products

def show_product_form():
    products = list_products(50)
    return get_template(f"""
        <h2>Articles</h2>
        <ul>
            {" ".join([f"""<li><a href="/products/remove/{product.id}">[x]</a> {product.id} - {product.name} </li>""" for product in products])}
        </ul>
        <h2>Enregistrement</h2>
        <form method="POST" action="/products/add">
            <label>Nom <input type="text" name="name" maxlength="100" required></label><br>
            <label>Numéro SKU <input type="text" name="sku" maxlength="64" required></label><br>
            <label>Prix unitaire <input type="number" name="price" step="0.01" value="1.00" min="0.00" max="99999.00"></label><br>
            <input type="submit" value="Enregistrer">
        </form>
    """)

def register_product(params):
    if len(params.keys()):
        name = get_param(params, "name")
        sku = get_param(params, "sku")
        price = get_param(params, "price")
        result = create_product(name, sku, price)
    else: 
        return get_template(f"""
                <h2>Erreur</h2>
                <code>La requête est vide</code>
            """)

    if isinstance(result, numbers.Number):
        return get_template(f"""
                <h2>Information: l'article {result} a été ajouté.</h2>
                <a href="/products">← Retourner à la page des articles</a>
            """)
    else:
        return get_template(f"""
                <h2>Erreur</h2>
                <code>{result}</code>
            """)
    
def remove_product(product_id):
    result = delete_product(product_id)
    if result:
        return get_template(f"""
            <h2>Information: l'article {product_id} a été supprimé.</h2>
            <a href="/products">← Retourner à la page des articles</a>
        """)
    else:
        return get_template(f"""
                <h2>Erreur</h2>
                <code>{result}</code>
            """)