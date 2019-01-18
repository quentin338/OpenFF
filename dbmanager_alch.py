import json
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from datetime import date

from alch_tables import Products, Categories, History
from CONSTANTS import products_json, username, host, dbname, number_of_categories, Base
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
            print('Catégories déjà créées ! ', end="")

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
            print("Produits déjà insérés !")

    def asking_categories(self):
        all_categories = self.session.query(Categories).all()

        print("\nListe des catégories :\n")

        for category in all_categories:
            print(f"\t {category.id}  {category.name}")

        user_input = input(f"\nVeuillez choisir votre catégorie : ")

        try:
            if int(user_input) in range(1, number_of_categories + 1):
                self._products_in_category(user_input)
            else:
                print(f"Entrée invalide. Veuillez choisir un nombre entre 1 et {number_of_categories}.")
                self.asking_categories()
        except ValueError:
            print(f"Entrée invalide. Veuillez choisir un nombre entre 1 et {number_of_categories} : ")
            self.asking_categories()

    def _products_in_category(self, category_id):
        distinct_names = self.session.query(Products.name.distinct()).filter(Products.category == category_id)\
                                               .order_by(desc(Products.note)).distinct(Products.name).limit(10)

        products_name = []
        for row in distinct_names:
            products_name.append(*row)

        print(f"\nChoisissez l'aliment que vous voulez remplacer : \n")

        for i, name in enumerate(products_name):
            print(f'{i + 1}  {name}')

        inp = input("\nVotre choix : ")

        try:
            if int(inp) in range(1, len(products_name) + 1):
                self._best_product(category_id, products_name[int(inp) - 1])
            else:
                print(f"Entrée invalide. Choisissez un nombre entre 1 et {len(products_name)}")
                self._products_in_category(category_id)
        except ValueError:
            print(f"Entrée invalide. Choisissez un nombre entre 1 et {len(products_name)}")
            self._products_in_category(category_id)

    def _best_product(self, category_id, initial_product_name):
        initial_product = self.session.query(Products).filter(Products.name == initial_product_name).first()

        best_product = self.session.query(Products).filter(Products.category == category_id) \
            .order_by(Products.note).first()

        product_shops = self.session.query(Products).filter(Products.name == best_product.name)
        product_shops_list = set([product.shop for product in product_shops])
        product_shops_list = ", ".join(product_shops_list)

        if initial_product.name != best_product.name:
            print(f"\n\tVous pouvez remplacer l'aliment '{initial_product.name}' par : '{best_product.name}'")
            print(f"\tCe produit a une note de {best_product.note} et est disponible dans le(s) magasin(s) {product_shops_list}.")
            print(f"\tPlus d'informations disponibles sur le produit ici : {best_product.url}\n")

            self._registering_product(initial_product, best_product)
        else:
            print(f'\nLe produit "{best_product.name}" est déjà le plus sain de sa catégorie.')
            print(f'Il a une note de {best_product.note} et est disponible dans le(s) magasin(s) {product_shops_list}')
            print(f"Plus d'informations disponibles sur le produit ici : {best_product.url}\n")

            self._menu()

    def _registering_product(self, initial_product, best_product):
        # TODO Make sure that the user can't register the same research twice

            inp = input(f"Voulez-vous enregistrer cette recherche ? 1 pour OUI, 2 pour NON : ")
            if inp == "1":
                self.session.add(History(id_initial_product=initial_product.id, id_new_product=best_product.id,
                                         date=date.today()))
                self.session.commit()
                print("\nLe résultat a été enregistré.")
                self._menu()
            elif inp == "2":
                self._menu()
            else:
                print("Entrée invalide.")
                self._registering_product(initial_product, best_product)

    def _menu(self):
        print("\n\t 1 Rechercher un nouveau produit.")
        print("\t 2 Voir vos aliments enregistrés.")
        print("\t 3 Quitter le programme.\n")

        inp = input("Votre choix : ")

        if inp == "1":
            self.asking_categories()
        elif inp == "2":
            self.show_historic()
        elif inp == "3":
            print("\nMerci d'avoir utilisé notre programme ! L'équipe Pur Beurre.")
            pass
        else:
            print("Entrée invalide, veuillez recommencer.")
            self._menu()

    def show_historic(self):
        # TODO
        pass

