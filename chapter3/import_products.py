import csv
from db import Model, Session, engine
from models import Product, Manufacturer


def main():
    Model.metadata.drop_all(engine)  # warning: this deletes all data!
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            with open('products.csv') as f:
                reader = csv.DictReader(f)
                all_manufacturers = {}

                for row in reader:
                    row['year'] = int(row['year'])

                    # this is a string instance
                    # remove this manufacturer string
                    manufacturer = row.pop('manufacturer')
                    p = Product(**row)

                    if manufacturer not in all_manufacturers:
                        entity = Manufacturer(name=manufacturer)
                        session.add(entity)
                        print(f"Added {entity}")
                        # string -> entity mapping
                        all_manufacturers[manufacturer] = entity
                    entity = all_manufacturers[manufacturer]
                    entity.products.append(p)


if __name__ == '__main__':
    main()
