from db import Session
from models import Product, Country, Manufacturer
from sqlalchemy import select, func

session = Session()


def product_with_countries():
    q = select(Product).where(Product.name == 'Timex Sinclair 1000')
    p = session.scalar(q)
    p.countries

    q = select(Country).where(Country.name == 'Portugal')
    c = session.scalar(q)
    c.products


def product_with_more_countries():
    num_countries = func.count(Country.id).label('num_countries')
    q = (select(Product, num_countries)
         .join(Product.countries)
         .group_by(Product)
         .having(num_countries >= 2)
         .order_by(Product.name)
         )
    session.execute(q).all()


def operators_in_uk():
    q = (select(Manufacturer)
         .join(Manufacturer.products)
         .join(Product.countries)
         .where(Country.name == 'UK')
         .distinct()
         .order_by(Manufacturer.name)
         )
    session.scalars(q).all()


def manufacturer_with_more_countries():
    # distinct countries is important
    # (Manufacturer, Product, Country) is distinct
    # but we need (Manufacturer, Country) to be distinct
    num_countries = func.count(Country.id.distinct()).label('num_countries')
    q = (select(Manufacturer, num_countries)
         .join(Manufacturer.products)
         .join(Product.countries)
         .group_by(Manufacturer)
         .having(num_countries >= 2)
         )
    session.execute(q).all()
