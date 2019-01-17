from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.dialects.mysql import INTEGER

from CONSTANTS import Base


class Categories(Base):

    __tablename__ = "categories"

    id = Column('id', INTEGER(display_width=2, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    name = Column('name', String(100), nullable=False)


class Products(Base):

    __tablename__ = "products"

    id = Column('id', INTEGER(display_width=5, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    category = Column('category', INTEGER(display_width=2, unsigned=True),
                      ForeignKey(Categories.id), nullable=False)
    name = Column('name', String(200), nullable=False)
    note = Column('note', INTEGER(display_width=2), nullable=False)
    shop = Column('shop', String(50), nullable=False)
    url = Column('url', String(150), nullable=False)

    def __init__(self, category, name, note, shop, url):
        self.category = category
        self.name = name
        self.note = note
        self.shop = shop
        self.url = url


class History(Base):

    __tablename__ = "history"

    id = Column('id', INTEGER(display_width=3, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    id_initial_product = Column('id_initial_product', INTEGER(display_width=5, unsigned=True),
                                ForeignKey(Products.id), nullable=False)
    id_new_product = Column('id_new_product', INTEGER(display_width=5, unsigned=True),
                            ForeignKey(Products.id), nullable=False)
    date = Column('date', Date, nullable=False)

    def __init__(self, id_initial_product, id_new_product, date):
        self.id_initial_product = id_initial_product
        self.id_new_product = id_new_product
        self.date = date