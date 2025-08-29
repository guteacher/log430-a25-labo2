"""
Product view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

def show_product_form():
    return """
    <!DOCTYPE html>
    <html lang="fr">
        <head>
            <meta charset="UTF-8">
        </head>
        <h1>Ajouter un nouveau article</h1>
        <form method="POST" action="/">
            <label>Nom: <input type="text" name="name"></label><br>
            <label>Numéro SKU: <input type="text" name="sku"></label><br>
            <label>Prix unitaire: <input type="number" name="price" step="0.01" value="1.00"></label><br>
            <input type="submit" value="OK">
        </form>
    </html>
    """