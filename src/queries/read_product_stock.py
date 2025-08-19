"""
Product (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session
from models.product_stock import ProductStock

def get_product_stock_by_id(product_id):
    """Get stock by product ID """
    session = get_sqlalchemy_session()
    return session.query(ProductStock).filter_by(id=product_id).all()

