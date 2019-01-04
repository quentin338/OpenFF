from os import listdir

from constants import products_json
from apimanager import APIManager


def main():

    if products_json not in listdir():
        api = APIManager()
        api.get_categories()
        api.output_to_json(api.products_data)
    else:
        print("Products already downloaded !")


if __name__ == "__main__":
    main()



    # creating_database()
    # creating_tables()
    # json to database()
    # inserting_products()
    # interactive program beginning()
