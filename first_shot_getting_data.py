import requests
import json
from os import listdir

from constants import products_json, number_of_products
from creating_database import creating_database, creating_tables, inserting_products


def get_products():

    products_data = {"products": []}

    if products_json not in listdir():

        ### Connecting to OpenFF and getting the first 10 categories ###

        all_categories = requests.get('https://fr.openfoodfacts.org/categories?json=true')
        first_ten_categories = all_categories.json()['tags'][:10]

        ### URL of categories are the names with "-" in between. Loop to work with one category at a time. ###

        for category in first_ten_categories:
            category_name = category["name"]
            category_name_for_url = category_name.replace(" ", "-")

            full_url = f"https://fr.openfoodfacts.org/cgi/search.pl" \
                f"?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0={category_name_for_url}" \
                f"&sort_by=unique_scans_n&page_size={number_of_products}&json=true"

        ### GET a list of X products from full_url ###

            all_products = requests.get(full_url)

            list_products = all_products.json()["products"]

        ### Excluding all products with no fr notes, no name, no stores + TBD ###

            for each_product in list_products:
                if '-- fr' in each_product['nutrition_score_debug'] and each_product['generic_name_fr'] != "" and each_product['stores_tags']:

                    ### Notes are on the form X | -X | XX at the end of the string

                    note_product = each_product['nutrition_score_debug'][len(each_product['nutrition_score_debug']) - 2:]
                    note_product = note_product.strip()

                    name_product = each_product['generic_name_fr']

                    selling_points = each_product['stores_tags']

                    product_url = each_product['url']

                    products_data['products'].append({
                             'category_name': category_name,
                             'name_product': name_product,
                             'note_product': note_product,
                             'selling points': selling_points,
                             'product_url': product_url})

                else:
                    pass

        try:
            output_to_json(products_data)
            print("All products outputted")
        except NameError:
            pass
    else:
        print('Products already downloaded to a json file')
        pass


def output_to_json(dict_to_dump):

    with open(products_json, 'a', encoding='utf-8') as outfile:
        json.dump(dict_to_dump, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_products()
# creating database()
    creating_database()
    creating_tables()
# json to database()
    inserting_products()
# interactive program beginning()
