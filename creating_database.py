import mysql.connector
from constants import host, dbname
from userpassdb import username, userpass


def creating_database():

    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=userpass
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname} CHARACTER SET 'utf8mb4'")


def creating_tables():

    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=userpass,
        database=dbname
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"USE {dbname}")

    mycursor.execute()


creating_database()
creating_tables()
