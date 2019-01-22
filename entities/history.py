from sqlalchemy import Column, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER

from entities.products import Products
from src.config import Base


class History(Base):
    """
    History table
    """

    __tablename__ = "history"

    id = Column('id', INTEGER(display_width=3, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    id_initial_product = Column('id_initial_product', INTEGER(display_width=5, unsigned=True),
                                ForeignKey(Products.id), nullable=False)
    id_new_product = Column('id_new_product', INTEGER(display_width=5, unsigned=True),
                            ForeignKey(Products.id), nullable=False)
    date = Column('date', DateTime, nullable=False)

    __table_args__ = (UniqueConstraint('id_initial_product', 'id_new_product', name='uc_saved_search'),)

    def __init__(self, id_initial_product, id_new_product, date):
        self.id_initial_product = id_initial_product
        self.id_new_product = id_new_product
        self.date = date
