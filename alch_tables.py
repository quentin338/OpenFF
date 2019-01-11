from sqlalchemy import create_engine, Column, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import INTEGER

from userpassdb import username, userpass
from constants import host, dbname


Base = declarative_base()


class test_categories(Base):

    __tablename__ = "test_categories"

    id = Column('id', INTEGER(display_width=2, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    category_name = Column('category_name', String(100), nullable=False)

    def __init__(self):
        pass


class test_products(Base):

    __tablename__ = "test_products"

    id = Column('id', INTEGER(display_width=5, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    category = Column('category', INTEGER(display_width=2, unsigned=True),
                      ForeignKey(test_categories.id), nullable=False)
    name = Column('name', String(200), nullable=False)
    note = Column('note', INTEGER(display_width=2), nullable=False)
    shops = Column('shops', String(50), nullable=False)
    url = Column('url', String(150), nullable=False)


class test_history(Base):

    __tablename__ = "test_history"

    id = Column('id', INTEGER(display_width=3, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    id_initial_product = Column('id_initial_product', INTEGER(display_width=5, unsigned=True),
                                ForeignKey(test_products.id), nullable=False)
    id_new_product = Column('id_new_product', INTEGER(display_width=5, unsigned=True),
                            ForeignKey(test_products.id), nullable=False)
    date = Column('date', Date, nullable=False)


engine = create_engine(f'mysql+mysqlconnector://{username}:{userpass}@{host}', echo=True)

engine.execute(f'CREATE DATABASE IF NOT EXISTS {dbname}')
engine.execute(f'USE {dbname}')

Session = sessionmaker(bind=engine)

session = Session()
Base.metadata.create_all(engine)
