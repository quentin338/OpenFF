from sqlalchemy.ext.declarative import declarative_base

# INSERT YOUR MYSQL INFO HERE

host = 'localhost'
username = 'root'
userpass = 'rootOC'

dbname = 'openfoodfacts'

# mysql-alchemy

Base = declarative_base()
