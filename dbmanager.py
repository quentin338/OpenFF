import mysql.connector
import json

from constants import host, dbname, products_json
from userpassdb import username, userpass
from tables import *


class Dbmanager:

    def __init__(self):
        self.host = host
        self.username = username
        self.password = userpass
        self.connect = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=userpass
        )

    def __enter__(self):
        return self.connect.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.commit()
        print("exit")

    def creating_database(self):
        with self as c:
            c.execute(f"CREATE DATABASE IF NOT EXISTS {dbname} CHARACTER SET 'utf8mb4'")
            c.execute(f'USE {dbname}')

    def creating_tables(self):
        for table_name in TABLES:
            table_description = TABLES[table_name]

            with self as c:
                c.execute(table_description)

    def inserting_products(self):
        with open(products_json, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            category_list = set()
            product_list = []

            for product in data['products']:
                category_name, name, note, selling, url = product.values()

                category_list.add((category_name,))

                for each_shop in selling:
                    if "β" not in each_shop:
                        product_list.append((name, note, each_shop, url, category_name))
                    else:
                        pass

            with self as c:
                try:
                    c.executemany(add_product_category, category_list)
                    print('Adding products to database...')
                    c.executemany(add_product, product_list)
                    print('Products added !')
                except ValueError:
                    pass


db = Dbmanager()
db.creating_database()
db.creating_tables()
db.inserting_products()
