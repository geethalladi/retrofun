from typing import Optional
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Model

# defining the join table
# Doing at the top, so that the secondary relationship reference
# could be done using this join table
# this uses core syntax for defining the table
ProductCountry = Table(
    'products_countries',
    Model.metadata,
    # specify column - foreign key at both the ends
    Column('product_id', ForeignKey('products.id'), primary_key=True,
           nullable=False),
    Column('country_id', ForeignKey('countries.id'), primary_key=True,
           nullable=False),
)


class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey('manufacturers.id'), index=True)
    year: Mapped[int] = mapped_column(index=True)
    cpu: Mapped[Optional[str]] = mapped_column(String(32))

    # manufacturer as 1:n (many end to one)
    manufacturer: Mapped['Manufacturer'] = relationship(
        back_populates='products')

    # countries as a many to many relationship
    # secondary specifies the external join table
    countries: Mapped[list['Country']] = relationship(
        secondary=ProductCountry,
        back_populates='products')

    def __repr__(self):
        return f'Product({self.id}, "{self.name}")'


class Manufacturer(Model):
    __tablename__ = 'manufacturers'

    # manufacturer with (id, name)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)

    # manufacturer as 1:n (one end to many)
    products: Mapped[list['Product']] = relationship(
        cascade='all, delete-orphan', back_populates='manufacturer')

    def __repr__(self):
        return f'Manufacturer({self.id}, "{self.name}")'


class Country(Model):
    __tablename__ = 'countries'

    # separate table for country
    # stores just the (id, name) attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)

    # Join Table and many to many relations
    # referencing the ProductCountry in `secondary`
    # secondary specifies the external join table
    # back_populates mentions on the other side
    products: Mapped[list['Product']] = relationship(
        secondary=ProductCountry,
        back_populates='countries')

    def __repr__(self):
        return f'Country({self.id}, "{self.name}")'
