from sqlalchemy import TIMESTAMP, Column, Integer, String, text
from app.database.db import Base  

class User(Base): 
    __tablename__ = 'users'  

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
