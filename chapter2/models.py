from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session
from db import Model, engine, SessionMaker


class Product(Model):
    # Plural table name
    __tablename__ = 'products'

    # use mapped_column for defining the column properties
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    manufacturer: Mapped[str] = mapped_column(String(64), index=True)

    # if no constraint needed just `year: Mapped[int]` is enough
    year: Mapped[Optional[int]]  # = mapped_column(index=True)

    country: Mapped[Optional[str]] = mapped_column(String(32))
    cpu: Mapped[Optional[str]] = mapped_column(String(32))

    def __repr__(self):
        return f'Product({self.id}, "{self.name}")'


def create_product_instance(engine):
    # Using engine
    # sqlalchemy.orm.Session
    # Use engine to create a session every time
    with Session(engine) as session:
        c64 = Product(name='Commodore 64', manufacturer='Commodore')
        try:
            # add / commit
            session.add(c64)
            session.commit()
        except Exception:
            # rollback the changes
            session.rollback()
            raise
        print(c64)


def create_product_instance_use_sessionmaker():
    c64 = Product(name='Commodore 64', manufacturer='Commodore')
    with SessionMaker() as session:
        # begin implements the try / catch and commit / rollback
        with session.begin():
            session.add(c64)
        print(c64)


def clean_db(engine):
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)


def clean():
    clean_db(engine)
