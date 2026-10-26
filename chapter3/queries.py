from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
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


def select_primary_key():
    p = session.get(Product, 27)
    p.name
    p.manufacturer_id
    p.manufacturer


def n_plus_1_queries():
    # default loader: select - lazy
    q = select(Product)
    ps = session.execute(q).all()
    for p in ps:
        print(p.name, p.manufacturer.name)
    # using joinedload loader - eager fetch
    # joinedload can be configured as part of relationship and back_populates
    # so every time a Product is obtained the Manufacturer is also loaded
    # and vice versa
    q = select(Product).options(joinedload(Product.manufacturer))
    ps = session.scalars(q).all()
    for p in ps:
        print(p.name, p.manufacturer.name)


def delete_cascade():
    p = session.get(Product, 24)
    session.delete(p)
    session.commit()

    # Try delete a manufacturer
    m = session.get(Manufacturer, 5)
    session.delete(m)
    # will not work - ForeignKey Constraint
    # session.commit()
    session.rollback()

    # Do it with relationship updated
    m = session.get(Manufacturer, 5)
    session.delete(m)
    # Once the relationship is updated on cascade='all, delete-orphan'
    session.commit()

    # Try getting Products with manufacturer_id = 5
    q = select(Product).where(Product.manufacturer_id == 5)
    # empty
    session.scalars(q).all()


def detach_relation():
    p = session.get(Product, 2)
    m = p.manufacturer
    # remove relation between m and p
    m.products.remove(p)
    # p is detached and deleted
    session.commit()
