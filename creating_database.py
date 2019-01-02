import mysql.connector
from constants import host, dbname
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


creating_database()
creating_tables()
