from db import SessionMaker
from models import Product
from sqlalchemy import select, or_

session = SessionMaker()


def select_filter():
    # defaults to 'and' condition
    q = (select(Product)
         .where(Product.manufacturer == 'Commodore')
         .where(Product.year >= 1980))
    session.scalars(q).all()

    # or condition
    q = (select(Product)
         .where(or_(Product.year < 1970, Product.year > 1990)))
    session.scalars(q).all()

    # like function
    q = (select(Product)
         .where(Product.name.like('%Sinclair%')))
    session.scalars(q).all()

    # between
    q = (select(Product)
         .where(Product.year.between(1970, 1990)))
    session.scalars(q).all()


def debug_query(q):
    print(q)
    # how the literals are being added to Prepared Statement
    print(q.compile(compile_kwargs={'literal_binds': True}))


def select_all():
    # select query
    q = select(Product)
    print(q)  # prints the sql

    # lazy result sets
    r = session.execute(q)
    print(list(r))

    # eager version
    session.execute(q).all()

    # Returns each row as a single scalar (Product)
    # To return all rows as [Product]
    session.scalars(q).all()

    # first / one / one_or_none
    session.execute(q).first()
    # when exactly one row is needed
    # don't use this if you have more rows
    session.execute(q).one()
    session.execute(q).one_or_none()

    # equivalent to scalars(q).first
    # scalar_one / scalar_one_or_none exists
    session.scalar(q)
