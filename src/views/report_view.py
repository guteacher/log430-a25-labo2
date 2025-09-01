"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template, get_param

def show_highest_spending_users():
    """ Show report of highest spending users """
    return get_template("<h2>Les plus grands acheteurs</h2><p>Liste avec nom, total depensé</p>")