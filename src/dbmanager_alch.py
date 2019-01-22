import json
from datetime import datetime
from colorama import init, ansi
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

import src.CONSTANTS as CONSTANTS
from entities.categories import Categories
from entities.history import History
from entities.products import Products
from src.config import host, username, userpass, dbname, Base


class Dbmanager:

    def __init__(self, session):
        self.session = session
        init(autoreset=True)

    @classmethod
    def creating_table(cls):
        engine = create_engine(f'mysql+mysqlconnector://{username}:{userpass}@{host}', echo=False)

        engine.execute(f'CREATE DATABASE IF NOT EXISTS {dbname}')
        engine.execute(f'USE {dbname}')

        session = sessionmaker(bind=engine)()
        Base.metadata.create_all(engine)
        session.commit()

        return Dbmanager(session)

    def inserting_categories(self):
        if len(self.session.query(Categories).all()) == 0:
            print(f'{CONSTANTS.GREEN}Création des catégories. ', end="")

            with open(f'{CONSTANTS.PRODUCTS_JSON_DIR}{CONSTANTS.PRODUCTS_JSON}', 'r', encoding='utf-8') as infile:
                data = json.load(infile)
                categories = set()

                for product in data["products"]:
                    categories.add(product['category_name'])

                for category in categories:
                    cat = Categories(name=category)
                    self.session.add(cat)

            self.session.commit()

        else:
            print(f'{CONSTANTS.GREEN}Catégories déjà créées ! ', end="")

    def inserting_products(self):
        if len(self.session.query(Products).all()) == 0:
            print(f'{CONSTANTS.GREEN}Insertion des produits.')

            with open(f'{CONSTANTS.PRODUCTS_JSON_DIR}{CONSTANTS.PRODUCTS_JSON}', 'r', encoding='utf-8') as infile:
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
            print(f"{CONSTANTS.GREEN}Produits déjà insérés !")

    def asking_categories(self):
        all_categories = self.session.query(Categories).all()

        print(ansi.clear_screen())
        print(f"\nListe des catégories :\n")
        for category in all_categories:
            print(f"\t {category.id}  {category.name}")

        user_input = input(f"\nVeuillez choisir votre catégorie : ")

        try:
            if int(user_input) in range(1, CONSTANTS.NUMBER_OF_CATEGORIES + 1):
                self._products_in_category(user_input)
            else:
                print(ansi.clear_screen())
                print(f"{CONSTANTS.RED}Entrée invalide. Veuillez choisir un nombre entre 1 et {CONSTANTS.NUMBER_OF_CATEGORIES}.")
                self.asking_categories()
        except ValueError:
            print(ansi.clear_screen())
            print(f"{CONSTANTS.RED}Entrée invalide. Veuillez choisir un nombre entre 1 et {CONSTANTS.NUMBER_OF_CATEGORIES} : ")
            self.asking_categories()

    def _products_in_category(self, category_id):
        distinct_names = self.session.query(Products.name.distinct()).filter(Products.category == category_id)\
                                               .order_by(desc(Products.note)).limit(10)

        products_name = []
        for row in distinct_names:
            products_name.append(*row)

        print(ansi.clear_screen())
        print(f"\nChoisissez l'aliment que vous voulez remplacer : \n")

        for i, name in enumerate(products_name):
            print(f'\t{i + 1}  {name}')

        inp = input("\nVotre choix : ")

        try:
            if int(inp) in range(1, len(products_name) + 1):
                self._best_product(category_id, products_name[int(inp) - 1])
            else:
                print(ansi.clear_screen())
                print(f"Entrée invalide. Choisissez un nombre entre 1 et {len(products_name)}")
                self._products_in_category(category_id)
        except ValueError:
            print(ansi.clear_screen())
            print(f"Entrée invalide. Choisissez un nombre entre 1 et {len(products_name)}")
            self._products_in_category(category_id)

    def _best_product(self, category_id, initial_product_name):
        initial_product = self.session.query(Products).filter(Products.name == initial_product_name).first()

        best_product = self.session.query(Products).filter(Products.category == category_id) \
            .order_by(Products.note).first()

        product_shops = self.session.query(Products).filter(Products.name == best_product.name)
        product_shops_list = set(product.shop for product in product_shops)
        product_shops_list = ", ".join(product_shops_list)

        if initial_product.name != best_product.name:
            print(f"\n\tVous pouvez remplacer l'aliment {CONSTANTS.RED}'{initial_product.name}'{CONSTANTS.RESET_COLOR} "
                  f"par : {CONSTANTS.LIGHT_GREEN}'{best_product.name}'")
            print(f"\tCe produit a une note de {CONSTANTS.LIGHT_GREEN}{best_product.note}{CONSTANTS.RESET_COLOR} et "
                  f"est disponible dans le(s) magasin(s) {CONSTANTS.GREEN}{product_shops_list}.")
            print(f"\tPlus d'informations disponibles sur le produit ici : {best_product.url}\n")

            self._registering_product(initial_product, best_product)
        else:
            print(f"\n\tLe produit {CONSTANTS.LIGHT_GREEN}'{best_product.name}'{CONSTANTS.RESET_COLOR} "
                  f"est déjà le plus sain de sa catégorie.")
            print(f'\tIl a une note de {CONSTANTS.LIGHT_GREEN}{best_product.note}{CONSTANTS.RESET_COLOR} et est disponible '
                  f'dans le(s) magasin(s) {CONSTANTS.GREEN}{product_shops_list}')
            print(f"\tPlus d'informations disponibles sur le produit ici : {best_product.url}\n")

            self.menu()

    def _registering_product(self, initial_product, best_product):
        inp = input(f"Voulez-vous enregistrer cette recherche ? 1 pour OUI, 2 pour NON : ")

        try:
            if inp == "1":
                self.session.add(History(id_initial_product=initial_product.id, id_new_product=best_product.id,
                                         date=datetime.now()))
                self.session.commit()
                print(ansi.clear_screen())
                print(f"\n{CONSTANTS.GREEN}Le résultat a été enregistré.")
                self.menu()
            elif inp == "2":
                print(ansi.clear_screen())
                self.menu()
            else:
                print(ansi.clear_screen())
                print(f"{CONSTANTS.RED}Entrée invalide.")
                self._registering_product(initial_product, best_product)
        except IntegrityError:
            print(ansi.clear_screen())
            print(f"\n{CONSTANTS.LIGHT_YELLOW}Cette recherche a déjà été enregistrée. Retrouvez-la en tapant 2 dans le menu.")
            self.session.rollback()
            self.menu()

    def menu(self, first_start=False):
        if first_start:
            print(f"\nBienvenue dans l'application {CONSTANTS.LIGHT_YELLOW}Pur Beurre{CONSTANTS.RESET_COLOR}, "
                  f"où vous pourrez substituer des aliments plus sains à vos envies !!")

        print(f"\n\t {CONSTANTS.LIGHT_GREEN}1 Substituer un nouvel aliment.")
        if len(self.session.query(History).all()) != 0:
            print(f"\t {CONSTANTS.LIGHT_BLUE}2 Voir vos recherches enregistrées.")
            print(f"\t {CONSTANTS.LIGHT_BLUE}E Effacer les recherches.")
        print(f"\t {CONSTANTS.RED}Q Quitter le programme.\n")

        inp = input("Votre choix : ")

        if inp in ["1", "2", "e", "q", "E", "Q"]:
            if inp == "1":
                self.asking_categories()
            elif inp.lower() == "q":
                print(ansi.clear_screen())
                print(f"\nMerci d'avoir utilisé notre programme ! L'équipe {CONSTANTS.LIGHT_YELLOW}Pur Beurre.")
            elif len(self.session.query(History).all()) != 0:
                if inp.lower() == "e":
                    self._delete_history()
                    self.menu()
                elif inp == "2":
                    self.show_history()
            else:
                print(ansi.clear_screen())
                print(f"{CONSTANTS.RED}Entrée invalide, veuillez recommencer.")
                self.menu()
        else:
            print(ansi.clear_screen())
            print(f"{CONSTANTS.RED}Entrée invalide, veuillez recommencer.")
            self.menu()

    def show_history(self):
        history_list = self.session.query(History).order_by(desc(History.date)).all()

        print(ansi.clear_screen())
        for row in history_list:
            initial_product = self.session.query(Products).filter(Products.id == row.id_initial_product).first()
            new_product = self.session.query(Products).filter(Products.id == row.id_new_product).first()

            print(f"\n\tNous vous proposons de remplacer le produit "
                  f"'{CONSTANTS.RED}{initial_product.name}'{CONSTANTS.RESET_COLOR} par {CONSTANTS.LIGHT_GREEN}'{new_product.name}'.")
            print(f"\tPlus d'informations disponibles sur ce produit ici : {new_product.url}")
            print("\t****")

        self.menu()

    def _delete_history(self):
        print(ansi.clear_screen())
        print(f"\n{CONSTANTS.LIGHT_BLUE}Vos recherches enregistrées ont été effacées !")

        self.session.query(History).delete()
        self.session.commit()
