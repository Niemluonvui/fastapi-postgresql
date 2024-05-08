from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    
class category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    
class country(Base):
    __tablename__ = "country"

    country_id = Column(Integer, primary_key=True)
    country_name = Column(String, unique=True, index=True)
    
    