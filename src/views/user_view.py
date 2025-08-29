"""
User view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from controllers.user_controller import create_user, remove_user, get_user

def show_user_form():
    return """
    <!DOCTYPE html>
    <html lang="fr">
        <head>
            <meta charset="UTF-8">
        </head>
        <h1>Ajouter un nouveau utilisateur</h1>
        <form method="POST" action="/">
            <label>Prénom: <input type="text" name="name"></label><br>
            <label>Addresse courriel: <input type="text" name="email"></label><br>
            <input type="submit" value="OK">
        </form>
    </html>
    """

def process_user_form(params):
    name = params.get("name")[0]
    email = params.get("email")[0]
    create_user(name, email)
    return f"""
        <h1>Utilisateur ajouté avec succès!</h1>
        <a href="/">Retourner</a>
    """