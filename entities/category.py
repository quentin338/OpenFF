from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER

from src.config import Base


class Category(Base):
    """
    Category table
    """

    __tablename__ = "category"

    id = Column('id', INTEGER(display_width=2, unsigned=True), nullable=False, autoincrement=True, primary_key=True)
    name = Column('name', String(100), nullable=False)
