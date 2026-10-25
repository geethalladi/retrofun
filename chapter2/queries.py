from db import SessionMaker
from models import Product
from sqlalchemy import select, or_, func

session = SessionMaker()


def deletion():
    pdt = session.get(Product, 23)
    session.delete(pdt)
    session.commit()


def select_by_id():
    # with where clause
    q = select(Product).where(Product.id == 23)
    session.scalar(q)
    # using session.get()
    result = session.get(Product, 23)
    print(result)


def pagination():
    # limit
    q = (select(Product)
         .order_by(Product.name)
         .limit(3))
    session.scalars(q).all()
    # limit / offset
    q = (select(Product)
         .order_by(Product.name)
         .offset(3)
         .limit(3))
    session.scalars(q).all()
    # limit / offset -> when rows are added / removed
    q = (select(Product)
         .order_by(Product.name)
         .limit(3)
         .where(Product.name > 'Acron Archimedes'))
    session.scalars(q).all()
    # when going back (instead of limit / offset)
    q = (select(Product)
         .order_by(Product.name.desc())
         .limit(3)
         .where(Product.name < 'Acorn Atom'))
    session.scalars(q).all()


def group_by():
    # group by to find the max / min years
    q = (select(Product.manufacturer,
                func.min(Product.year),
                func.max(Product.year),
                func.count())
         .group_by(Product.manufacturer)
         .order_by(Product.manufacturer))
    session.execute(q).all()
    # group_by and having
    q = (select(Product.manufacturer,
                func.count())
         .group_by(Product.manufacturer)
         .having(func.count() >= 5)
         .order_by(Product.manufacturer))
    session.execute(q).all()
    # specify a label to remove redundancy above
    num_products = func.count().label('num_products')
    q = (select(Product.manufacturer,
                num_products)
         .group_by(Product.manufacturer)
         .having(num_products >= 5)
         .order_by(Product.manufacturer))
    session.execute(q).all()
    # first, last year, num_products in Croatia
    q = (select(func.min(Product.year),
                func.max(Product.year),
                func.count(Product.id))
         .where(Product.country == 'Croatia')
         .group_by(Product.country))
    session.execute(q).all()
    # num_products each year
    num_products = func.count().label('num_products')
    q = (select(Product.year, num_products)
         .group_by(Product.year)
         .order_by(num_products.desc())
         .having(num_products > 0)
         )
    session.execute(q).all()


def aggregates():
    # count
    q = select(func.count(Product.id))
    session.scalar(q)
    # another form
    q = select(func.count()).select_from(Product)
    session.scalar(q)
    # min / max
    q = select(func.min(Product.year), func.max(Product.year))
    session.execute(q).first()
    # distinct
    q = select(Product.manufacturer).order_by(Product.manufacturer).distinct()
    session.execute(q).all()
    # distinct count
    q = select(func.count(Product.manufacturer.distinct()))
    session.scalar(q)
    # manufacturers in 1980s
    q = (select(Product.manufacturer).distinct()
         .where(Product.year.between(1980, 1989)))
    session.scalars(q).all()
    # 'T' manufacturers
    q = (select(Product.manufacturer.distinct())
         .where(Product.manufacturer.like('T%'))
         .order_by(Product.manufacturer.asc()))
    session.scalars(q).all()
    # USA manufacturers
    q = (select(func.count(Product.manufacturer.distinct()))
         .where(Product.country == 'USA'))
    session.scalar(q)


def order_by():
    q = (select(Product)
         .order_by(Product.name))
    session.scalars(q).all()
    q = (select(Product)
         .order_by(Product.year.desc()))
    session.scalars(q).all()
    # order by multiple columns
    q = (select(Product)
         .order_by(Product.year.desc(), Product.year.asc()))
    session.scalars(q).all()
    # Product with Z80 CPU or 6502 CPU
    q = (select(Product)
         .where(or_(Product.cpu.like('%Z80%'), Product.cpu.like('%6502%')))
         .where(Product.year < 1990)
         .order_by(Product.name.asc()))
    session.scalars(q).all()


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

    # first 3 Products by name built in 1983
    q = (select(Product)
         .where(Product.year == 1983)
         .limit(3)
         .order_by(Product.name.asc()))
    session.scalars(q).all()

    # Product with Z80 CPU
    q = (select(Product)
         .where(Product.cpu.like('%Z80%')))
    session.scalars(q).all()


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

    # select columns
    q = select(Product.name, Product.year)
    session.execute(q).all()


def debug_query(q):
    print(q)
    # how the literals are being added to Prepared Statement
    print(q.compile(compile_kwargs={'literal_binds': True}))
