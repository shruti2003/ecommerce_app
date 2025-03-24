from array import array
import datetime
from typing import List, Optional
from pydantic import BaseModel, SkipValidation

class UserCreate(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True  


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True  
        arbitrary_types_allowed = True


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int

    class Config:
        from_attributes = True  


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int

    class Config:
        from_attributes = True  


class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    products: List[int]


    class Config:
        from_attributes = True  


class OrderOut(BaseModel):
    customer_name: str
    customer_email: str
    products: List[int]
    total_price: float

    class Config:
        from_attributes = True  
        

class Token(BaseModel):
    access_token: str
    token_type: str

    

class TokenData(BaseModel):
    id: Optional[str] = None
