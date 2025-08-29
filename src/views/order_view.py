"""
Order view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

def show_order_form():
    return """
    <!DOCTYPE html>
    <html lang="fr">
        <head>
            <meta charset="UTF-8">
        </head>
        <h1>Ajouter une nouvelle commande</h1>
        <form method="POST" action="/">
            <label>Articles à commander: <input type="text" name="name"></label><br>
        </form>
    </html>
    """