"""
Template view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

def get_param(params, name):
    if not params or not name or not params.get(name):
        return ""
    return params.get(name)[0]

def get_template(content):
    return f"""<!DOCTYPE html>
    <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="/form.css">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <h1>Le Magasin du Coin</h1>
            <a href="/">← Retourner à la page d'accueil</a>
            <hr>
            {content}
        </body>
    </html>
    """