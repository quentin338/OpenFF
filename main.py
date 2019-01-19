from os import listdir

from CONSTANTS import products_json
from apimanager import APIManager
from dbmanager_alch import Dbmanager


class Main:
    def __init__(self):
        if products_json not in listdir():
            api = APIManager()
            api.get_categories()
            api.output_to_json(api.products_data)
        else:
            print("Produits déjà téléchargés ! ", end="")

        self.initdb()

    def initdb(self):
        db = Dbmanager.creating_table()
        db.inserting_categories()
        db.inserting_products()
        db.menu(first_start=True)


if __name__ == "__main__":

    db = Main()
