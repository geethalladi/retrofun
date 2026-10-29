import csv
from sqlalchemy import delete
from db import Session, Model, engine
from models import Product, Manufacturer, Country, ProductCountry


def main():
    # this works better
    Model.metadata.drop_all(engine)  # warning: this deletes all data!
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            session.execute(delete(ProductCountry))
            session.execute(delete(Product))
            session.execute(delete(Manufacturer))
            session.execute(delete(Country))

    with Session() as session:
        with session.begin():
            with open('products.csv') as f:
                reader = csv.DictReader(f)
                all_manufacturers = {}
                all_countries = {}

                for row in reader:
                    row['year'] = int(row['year'])

                    manufacturer = row.pop('manufacturer')
                    countries = row.pop('country').split('/')
                    p = Product(**row)

                    if manufacturer not in all_manufacturers:
                        m = Manufacturer(name=manufacturer)
                        session.add(m)
                        all_manufacturers[manufacturer] = m

                    # get the manufacturer
                    m = all_manufacturers[manufacturer]
                    # add this product to the manufacturers list
                    m.products.append(p)
                    # other side is implicit
                    # p.manufacturer = m

                    for country in countries:
                        if country not in all_countries:
                            c = Country(name=country)
                            session.add(c)
                            all_countries[country] = c
                        # get the country
                        c = all_countries[country]
                        # add this product to this country
                        c.products.append(p)
                        # other side is implicit
                        # p.countries.append(c)


if __name__ == '__main__':
    main()
