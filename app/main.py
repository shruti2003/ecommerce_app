import datetime
import random
from fastapi import FastAPI, status, Depends
from app.auth import auth
from app.routers import order, product, user, auth
from app.schemas import schemas 

from sqlalchemy.orm import Session
from app.database.db import SessionLocal




app = FastAPI()

app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(auth.router)




