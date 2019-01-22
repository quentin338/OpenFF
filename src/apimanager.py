import json
import requests

from src.CONSTANTS import PRODUCTS_JSON, NUMBER_OF_PRODUCTS, NUMBER_OF_CATEGORIES, PRODUCTS_JSON_DIR, GREEN


class APIManager:

    def __init__(self):
        self.products_data = {"products": []}

    def get_categories(self):
        print(f"{GREEN}Téléchargement des produits sur Openfoodfacts.org...", end="")

        all_categories_list = requests.get('https://fr.openfoodfacts.org/categories?json=true')
        categories = all_categories_list.json()['tags'][:NUMBER_OF_CATEGORIES]

        for category in categories:
            category_name = category["name"]
            category_name_for_url = category_name.replace(" ", "-")

            full_url = f"https://fr.openfoodfacts.org/cgi/search.pl" \
                f"?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=\
                    {category_name_for_url}&sort_by=unique_scans_n&page_size={NUMBER_OF_PRODUCTS}&json=true"

            all_products = requests.get(full_url)
            list_products = all_products.json()["products"]
            print(".", end="")
            self.get_products(list_products, category_name)

    def get_products(self, list_products, category_name):
        for each_product in list_products:
            if '-- fr' in each_product['nutrition_score_debug'] and \
                    each_product['product_name_fr'] != "" \
                    and each_product['stores_tags']:

                ### Notes are on the form X | -X | XX at the end of the string

                note_product = each_product['nutrition_score_debug']\
                                           [len(each_product['nutrition_score_debug']) - 2:]
                note_product = note_product.strip()

                name_product = each_product['product_name_fr']
                selling_points = each_product['stores_tags']
                product_url = each_product['url']

                self.products_data['products'].append({
                    'category_name': category_name,
                    'product_name': name_product,
                    'note': note_product,
                    'selling points': selling_points,
                    'product_url': product_url})
            else:
                pass

    def output_to_json(self, dict_to_dump):
        with open(f'{PRODUCTS_JSON_DIR}{PRODUCTS_JSON}', 'a', encoding='utf-8') as outfile:
            json.dump(dict_to_dump, outfile, ensure_ascii=False, indent=4)

            print(f"\n{GREEN}{len(self.products_data['products'])} produits exportés vers {PRODUCTS_JSON} !")
