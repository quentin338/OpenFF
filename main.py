from os import listdir

from constants import products_json
from apimanager import APIManager
from dbmanager_alch import Dbmanager


def main():

    if products_json not in listdir():
        api = APIManager()
        api.get_categories()
        api.output_to_json(api.products_data)
    else:
        print("Products already downloaded !")

    cnx = Dbmanager.creating_table()

    cnx.inserting_categories()
    cnx.inserting_products()
    cnx.asking_categories()


if __name__ == "__main__":
    main()
