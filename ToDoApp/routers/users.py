from fastapi import APIRouter, Depends, HTTPException, Path
from models import Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class PasswordRequest(BaseModel):
    pass


@router.get('/get_user', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    return user_model


@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency)
   if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')
    password_model = db.query(Users).filter(Users.id == user.get('id')).first()
