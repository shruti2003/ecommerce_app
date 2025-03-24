import random
import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app import models
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


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user