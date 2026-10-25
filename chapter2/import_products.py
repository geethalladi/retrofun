import csv
from db import Model, engine
from db import SessionMaker as Session
from models import Product


def main():
    Model.metadata.drop_all(engine)  # warning: this deletes all data!
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            with open('products.csv') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['year'] = int(row['year'])
                    # create Product Instance
                    product = Product(**row)
                    # Add to the DB
                    session.add(product)


if __name__ == '__main__':
    main()
