import random
import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from app.schemas import schemas
from app.database.db import get_db
from app.models.user import User
from app.utils.hash_password import hash  



router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    new_user = User(
        email=user.email,
        password=hashed_password  
    )

    db.add(new_user)
    db.commit()  
    db.refresh(new_user)

    return new_user  

