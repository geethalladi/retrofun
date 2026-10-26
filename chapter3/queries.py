from sqlalchemy import select, func, not_
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

    # Products made by IBM and Texas Instruments
    q = (select(Product)
         .join(Product.manufacturer)
         .where(Manufacturer.name.in_(["IBM", "Texas Instruments"])))
    session.scalars(q).all()

    # Operators in Brazil
    q = (select(Manufacturer)
         .distinct()
         .join(Manufacturer.products)
         .where(Product.country == 'Brazil'))
    session.scalars(q).all()

    # Manufacturer with products based on Z80
    q = (select(Manufacturer)
         .distinct()
         .join(Manufacturer.products)
         .where(Product.cpu.like('%Z80%')))
    session.scalars(q).all()

    # Manufacturer with products not based on 6502
    q = (select(Manufacturer)
         .distinct()
         .join(Manufacturer.products)
         .where(not_(Product.cpu.like('%6502%'))))
    session.scalars(q).all()

    # Manufacturer when they went live
    min_year = func.min(Product.year).label('min_year')
    q = (select(Manufacturer.name, min_year)
         .join(Product.manufacturer)
         .order_by(min_year.asc())
         .group_by(Manufacturer.name))
    session.execute(q).all()

    # Manufacturers with 3-5 products
    num_products = func.count(Product.id).label('num_products')
    q = (select(Manufacturer)
         .join(Manufacturer.products)
         .group_by(Manufacturer)
         .having(num_products.between(3, 5))
         )
    session.scalars(q).all()

    # Manufacturer operated for more than 5 years
    min_year = func.min(Product.year).label('min_year')
    max_year = func.max(Product.year).label('max_year')
    q = (select(Manufacturer)
         .join(Manufacturer.products)
         .group_by(Manufacturer)
         .having((max_year - min_year) > 5))
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
