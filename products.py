import json

from constants import products_json


class Product:

    list_products = []

    def __init__(self, category, name, note, shop, url):
        self.category = category
        self.name = name
        self.note = note
        self.shop = shop
        self.url = url

    @classmethod
    def spawning_products(cls):

        with open(products_json, 'r', encoding='utf-8') as infile:
            data = json.load(infile)

            for product in data['products']:
                product_object = Product(product['category_name'], product['name_product'], product['note_product'], product['selling points'], product['product_url'])
                cls.list_products.append(product_object)
