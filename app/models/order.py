from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ARRAY, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)  
    customer_name = Column(String)  
    customer_email = Column(String, unique=True, index=True) 
    total_price = Column(Float)  
    products = Column(ARRAY(Integer))  
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))  
