from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models
from app.database.db import get_db  

from app.auth import auth
from app.schemas import schemas
from app.models.user import User
from app.utils import hash_password



router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not hash_password.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = auth.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}



# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMiwiZXhwIjoxNzQyODM1Mjc5fQ.DD9TduCLB7g5zdW7QefJmJiBMjCbiMWPe7OfLhrgOSM",
#   "token_type": "bearer"
# }