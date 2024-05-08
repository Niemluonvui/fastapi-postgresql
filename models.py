from sqlalchemy import Column, Integer, String

from database import Base

class Category(Base):
    __tablename__ = "category"

    id = Column("category_id",Integer, primary_key=True)
    name = Column("name",String, unique=True, index=True)
    
class Country(Base):
    __tablename__ = "country"

    id = Column("country_id",Integer, primary_key=True)
    name = Column("country",String, unique=True, index=True)
    
tables_dict = {
    "category": Category,
    "country": Country,
    # Add more tables here
}