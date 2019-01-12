from alch_tables import Products, Categories, History
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json
from constants import products_json, username, host, dbname, number_of_categories, Base
from userpassdb import userpass


class Dbmanager:

    def __init__(self, session):
        self.session = session

    @classmethod
    def creating_table(cls):
        engine = create_engine(f'mysql+mysqlconnector://{username}:{userpass}@{host}', echo=False)

        engine.execute(f'CREATE DATABASE IF NOT EXISTS {dbname}')
        engine.execute(f'USE {dbname}')

        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(engine)
        session.commit()

        return Dbmanager(session)

    def inserting_categories(self):
        if len(self.session.query(Categories).all()) == 0:

            with open(products_json, 'r', encoding='utf-8') as infile:
                data = json.load(infile)
                categories = set()

                for product in data["products"]:
                    categories.add(product['category_name'])

                for category in categories:
                    cat = Categories(name=category)
                    self.session.add(cat)

            self.session.commit()

        else:
            print('Categories already inserted !')

    def inserting_products(self):
        if len(self.session.query(Products).all()) == 0:

            with open(products_json, 'r', encoding='utf-8') as infile:
                data = json.load(infile)

                for each_product in data['products']:
                    for each_shop in each_product['selling points']:
                        if "β" not in each_shop:
                            cat, name, note, _, url = each_product.values()

                            category_id = self.session.query(Categories).filter(Categories.name == cat)

                            for row in category_id:
                                self.session.add(Products(row.id, name, note, each_shop, url))

            self.session.commit()
        else:
            print("Products already inserted !")

    def asking_categories(self):
        all_categories = self.session.query(Categories).all()

        print("Liste des catégories :")

        for category in all_categories:
            print(category.id, category.name)

        user_input = input(f"Veuillez choisir votre catégorie : ")

        try:
            if int(user_input) in range(1, number_of_categories + 1):
                category_name = self.session.query(Categories).filter(Products.category == user_input).first()
                category_name = category_name.name
                self._best_product(user_input, category_name)
            else:
                print(f"Veuillez choisir un nombre entre 1 et {number_of_categories}.")
                self.asking_categories()
        except ValueError:
            print(f"Veuillez choisir un nombre entre 1 et {number_of_categories} : ")
            self.asking_categories()

    def _best_product(self, user_input, category_name):
        best_product = self.session.query(Products).filter(Products.category == user_input)\
                                                        .order_by(Products.note).first()

        product_shops = self.session.query(Products).filter(Products.name == best_product.name)
        product_shops_list = set([product.shop for product in product_shops])
        product_shops_list = ", ".join(product_shops_list)

        print(f"Le produit le plus sain de la catégorie {category_name} est : {best_product.name}")
        print(f"Ce produit a une note de {best_product.note} et est disponible dans le(s) magasins {product_shops_list}.")
        print(f"Plus d'informations disponibles sur le produit ici : {best_product.url}")


# cnx = Dbmanager.creating_table()
