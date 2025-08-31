"""
User view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import numbers
from views.template_view import get_template, get_param
from controllers.user_controller import create_user, delete_user, list_users

def show_user_form():
    users = list_users(10)
    return get_template(f"""
        <h2>Utilisateurs</h2>
        <p>Les 10 derniers enregistrements</p>
        <ul>
            {" ".join([f"""<li><a href="/users/remove/{user.id}">[x]</a> {user.id} - {user.name} </li>""" for user in users])}
        </ul>
        <h2>Enregistrement</h2>
        <form method="POST" action="/users/add">
            <label>Prénom <input type="text" name="name" maxlength="100" required></label><br>
            <label>Adresse courriel <input type="email" name="email" maxlength="150" required></label><br>
            <input type="submit" value="Enregistrer">
        </form>
    """)

def register_user(params):
    if len(params.keys()):
        name = get_param(params, "name")
        email = get_param(params, "email")
        result = create_user(name, email)
    else: 
        return get_template(f"""
                <h2>Erreur</h2>
                <code>La requête est vide</code>
            """)

    if isinstance(result, numbers.Number):
        return get_template(f"""
                <h2>Information: l'utilisateur {result} a été ajouté.</h2>
                <a href="/users">← Retourner à la page des utilisateurs</a>
            """)
    else:
        return get_template(f"""
                <h2>Erreur</h2>
                <code>{result}</code>
            """)
    
def remove_user(user_id):
    result = delete_user(user_id)
    if result:
        return get_template(f"""
            <h2>Information: l'utilisateur {user_id} a été supprimé.</h2>
            <a href="/users">← Retourner à la page des utilisateurs</a>
        """)
    else:
        return get_template(f"""
                <h2>Erreur</h2>
                <code>{result}</code>
            """)