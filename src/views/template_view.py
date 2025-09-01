"""
Template view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from controllers.order_controller import populate_redis_from_mysql

def show_main_menu():
    """ Show main menu, populate Redis if needed """
    populate_redis_from_mysql()
    return get_template("""
        <nav>
            <ul>
                <li><a href="/users">Utilisateurs</a></li>
                <li><a href="/products">Articles</a></li>
                <li><a href="/orders">Commandes</a></li>
            </ul>
        </nav>""", homepage=True)

def get_param(params, name):
    """ Get and sanitize paramters from request """
    if not params or not name or not params.get(name):
        return ""
    return params.get(name)[0]

def get_template(content, homepage=False):
    """ Inject content into base HTML template for the application """
    breadcrumb_text = """<p>Menu principal</p>""" if homepage else """<a href="/">← Retourner à la page d'accueil</a>"""
    return f"""<!DOCTYPE html>
    <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="/form.css">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <h1>Le Magasin du Coin</h1>
            {breadcrumb_text}
            <hr>
            {content}
        </body>
    </html>
    """