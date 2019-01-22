from os import listdir, mkdir

from src.CONSTANTS import PRODUCTS_JSON, PRODUCTS_JSON_DIR, GREEN
from src.apimanager import APIManager
from src.dbmanager_alch import Dbmanager, ansi, init


class Main:
    """
    Initializes API connection, DB connection and user program
    """

    def __init__(self):
        try:
            mkdir(PRODUCTS_JSON_DIR)
            print(f'{GREEN}Creating "{PRODUCTS_JSON_DIR}" directory...')
        except FileExistsError:
            pass

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
        """
        Initializes DB connection, creation, tables insertions and user program
        """

        database = Dbmanager.creating_table()
        database.inserting_categories()
        database.inserting_products()
        database.menu(first_start=True)


if __name__ == "__main__":

    DB = Main()
