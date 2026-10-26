from sqlalchemy import select, func
from db import Session
from models import Product, Manufacturer

session = Session()


def select_filter():
    q = select(Product).where(Product.name == 'ZX Spectrum')
    p = session.scalar(q)
    p.manufacturer.name
    # list all products
    p.manufacturer.products
    # Products from Texas Instruments
    q = select(Manufacturer).where(Manufacturer.name == 'Texas Instruments')
    m = session.scalar(q)
    m.products


def join():
    # join to list (Product.name, Manufacturer.name)
    # join when multiple tables are involved
    q = (select(Product.name, Manufacturer.name)
         .join(Manufacturer.products))
    # .join(Product.manufacturer))
    session.execute(q).all()
    # Manufacturer and count of Products
    num_products = func.count(Product.id).label('num_products')
    q = (select(Manufacturer.name, num_products)
         .group_by(Manufacturer.name)
         .order_by(Manufacturer.name)
         .join(Manufacturer.products)
         )
    session.execute(q).all()
