from sqlalchemy.ext.declarative import declarative_base

number_of_categories = 10
number_of_products = 20
products_json = 'products_output.json'

# MYSQL STUFF

host = 'localhost'
username = 'root'
userpass = ''

dbname = 'openfoodfacts'

# mysql-alchemy

Base = declarative_base()
