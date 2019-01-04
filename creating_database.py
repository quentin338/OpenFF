import mysql.connector
import json

from constants import host, dbname, products_json
from userpassdb import username, userpass
from tables import *


def creating_database():

    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=userpass
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname} CHARACTER SET 'utf8mb4'")

    mycursor.close()
    mydb.close()


def creating_tables():

    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=userpass,
        database=dbname
    )

    mycursor = mydb.cursor()

    ### Creating tables

    for table_name in TABLES:
        table_description = TABLES[table_name]
        mycursor.execute(table_description)

    mycursor.close()
    mydb.close()


def inserting_products():

    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=userpass,
        database=dbname
    )

    mycursor = mydb.cursor()

    ### Inserting products

    with open(products_json, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
        category_list = set()
        product_list = []

        for product in data['products']:
            category_name, name, note, selling, url = product.values()

            category_list.add((category_name,))

            for each_shop in selling:
                if "β" not in each_shop:   # Some Greek shop translated to ??? in SQL
                    product_list.append((name, note, each_shop, url, category_name))
                else:
                    pass

        try:
            mycursor.executemany(add_product_category, category_list)
            print('Adding products to database...')
            mycursor.executemany(add_product, product_list)
            print('Products added !')
            mydb.commit()
        except ValueError:
            pass

    mycursor.close()
    mydb.close()


# inserting_products()
