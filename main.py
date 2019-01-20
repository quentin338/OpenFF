from os import listdir

from src.CONSTANTS import PRODUCTS_JSON, PRODUCTS_JSON_DIR, GREEN
from src.apimanager import APIManager
from src.dbmanager_alch import Dbmanager, ansi, init


class Main:
    def __init__(self):
        if PRODUCTS_JSON not in listdir(PRODUCTS_JSON_DIR):
            api = APIManager()
            api.get_categories()
            api.output_to_json(api.products_data)
        else:
            init()
            print(ansi.clear_screen())
            print(f"{GREEN}Produits déjà téléchargés ! ", end="")

        self.initdb()

    @staticmethod
    def initdb():
        database = Dbmanager.creating_table()
        database.inserting_categories()
        database.inserting_products()
        database.menu(first_start=True)


if __name__ == "__main__":

    DB = Main()
