import requests
import json
from os import listdir

from constants import products_json, number_of_products, number_of_categories
# from creating_database import creating_database, creating_tables, inserting_products


class APIManager:

    products_data = {"products": []}
    categories_counter = 0

    def __init__(self):
        pass

    @classmethod
    def get_categories(cls):

        if products_json not in listdir():

            print("Getting products from OpenFoodFacts API...")

            all_categories_list = requests.get('https://fr.openfoodfacts.org/categories?json=true')
            categories = all_categories_list.json()['tags'][:number_of_categories]

            for category in categories:
                category_name = category["name"]
                category_name_for_url = category_name.replace(" ", "-")

                full_url = f"https://fr.openfoodfacts.org/cgi/search.pl" \
                    f"?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0={category_name_for_url}" \
                    f"&sort_by=unique_scans_n&page_size={number_of_products}&json=true"

                all_products = requests.get(full_url)

                list_products = all_products.json()["products"]

                cls.categories_counter += 1

                cls.get_products(list_products, category_name)

        else:
            print('Products already downloaded to a json file !!')
            pass

    @classmethod
    def get_products(cls, list_products, category_name):

        for each_product in list_products:
            if '-- fr' in each_product['nutrition_score_debug'] and each_product['generic_name_fr'] != "" \
                    and each_product['stores_tags']:

                ### Notes are on the form X | -X | XX at the end of the string

                note_product = each_product['nutrition_score_debug'][len(each_product['nutrition_score_debug']) - 2:]
                note_product = note_product.strip()

                name_product = each_product['generic_name_fr']
                selling_points = each_product['stores_tags']
                product_url = each_product['url']

                cls.products_data['products'].append({
                         'category_name': category_name,
                         'name_product': name_product,
                         'note_product': note_product,
                         'selling points': selling_points,
                         'product_url': product_url})
            else:
                pass

        try:
            if cls.categories_counter == number_of_categories:
                print('Outputting products to json...')
                cls.output_to_json(cls.products_data)
                print("All products outputted !")
            else:
                pass
        except NameError:
            pass

    @classmethod
    def output_to_json(cls, dict_to_dump):

        with open(products_json, 'a', encoding='utf-8') as outfile:
            json.dump(dict_to_dump, outfile, ensure_ascii=False, indent=4)

        # cls.creating_products_objects(dict_to_dump)

    @classmethod
    def creating_products_objects(cls, dict_of_products):

        for product in dict_of_products:
            print(product)


if __name__ == "__main__":
    APIManager.get_categories()
# creating database()
#     creating_database()
#     creating_tables()
# json to database()
#     inserting_products()
# interactive program beginning()
