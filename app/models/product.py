from app.database.db import Base  
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String


class Product(Base):
    __tablename__ = 'products'  
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, unique=True, index=True)
    price = Column(Float, unique=True, index=True)
    stock_quantity = Column(Integer, unique=True, index=True)

