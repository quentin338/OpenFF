from os import listdir

from constants import products_json
from apimanager import APIManager
from products import Product
from dbmanager import Dbmanager


def main():

    if products_json not in listdir():
        api = APIManager()
        api.get_categories()
        api.output_to_json(api.products_data)
    else:
        print("Products already downloaded !")

    Product.spawning_products()

    db = Dbmanager()
    db.creating_database()
    db.creating_tables()
    db.inserting_products(Product.list_products)


if __name__ == "__main__":
    main()



    # creating_database()
    # creating_tables()
    # json to database()
    # inserting_products()
    # interactive program beginning()
