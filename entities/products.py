from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER

from entities.categories import Categories
from src.config import Base


class Products(Base):
    """
    Product table
    """

    __tablename__ = "products"

    id = Column('id', INTEGER(display_width=5, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    category = Column('category', INTEGER(display_width=2, unsigned=True),
                      ForeignKey(Categories.id), nullable=False)
    name = Column('name', String(200), nullable=False)
    note = Column('note', INTEGER(display_width=2), nullable=False)
    shop = Column('shop', String(60), nullable=False)
    url = Column('url', String(150), nullable=False)

    def __init__(self, category, name, note, shop, url):
        self.category = category
        self.name = name
        self.note = note
        self.shop = shop
        self.url = url
