import mysql.connector

from constants import host, dbname
from userpassdb import username, userpass
from tables import *
from products import Product


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
        try:
            self.connect.commit()
            print("exit")
        except mysql.connector.errors.InternalError:
            print("Nothing to commit")

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
            c.execute("SELECT COUNT(*) FROM products")
            products_in_db = c.fetchone()
            products_in_db = products_in_db[0]

            if products_in_db == 0:
                try:
                    c.executemany(add_product_category, category_list)
                    print('Adding products to database...')
                    c.executemany(add_product, product_detail)
                    print('Products added !')
                except ValueError:
                    pass
            else:
                print("Products already in the database !")

    def finding_best_product(self):
        with self as c:
            c.execute(all_categories)

            category_list = c.fetchall()

            print(f"Liste des catégories :")

            for category in category_list:
                number, cat = category
                print(number, cat)

            user_input = input(f"Veuillez choisir votre catégorie : ")

            c.execute(best_product_in_category, (user_input,))
            best_product = Product(*c.fetchone())

            print(f"Le produit le plus sain de la catégorie {best_product.category} est : {best_product.name}")
            print(f"Ce produit a une note de {best_product.note} et est disponible dans le(s) magasins {best_product.shop}.")
            print(f"Plus d'informations disponibles sur le produit ici : {best_product.url}")

            return best_product


# db = Dbmanager()
