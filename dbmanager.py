import mysql.connector

from constants import host, dbname
from userpassdb import username, userpass
from tables import *
# from products import Product


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

    def inserting_products(self, products_list):

        category_list = set()
        product_detail = []

        for product in products_list:
            category_list.add((product.category,))

            for each_shop in product.shop:
                if "β" not in each_shop:
                    product_detail.append((product.name, product.note, each_shop, product.url, product.category))

        with self as c:
            try:
                c.executemany(add_product_category, category_list)
                print('Adding products to database...')
                c.executemany(add_product, product_detail)
                print('Products added !')
            except ValueError:
                pass


# Product.spawning_products()
#
# db = Dbmanager()
# db.creating_database()
# db.creating_tables()
# db.inserting_products(Product.list_products)
