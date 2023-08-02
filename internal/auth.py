### internal/auth.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import User, Admin
from config import Settings
import firebasescrypt

from internal.custom_exception import ItemKeyValidationError, ForeignKeyValidationError
from internal.schema import *
from internal.crudf import *

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
setting = Settings()

salt_separator = setting.fb_salt_separator
signer_key = setting.fb_signer_key
rounds = setting.fb_rounds
mem_cost = setting.fb_mem_cost

class User(BaseModel):
    email: str
    username: str | None = None
    status: bool
    valid: bool

# /auth 경로에 대한 핸들러 함수
@router.get("/")
async def get_auths(
        db: Session = Depends(get_db)
):
    auths = db.query(User).all()
    return auths

# 로그인
@router.post("/login")
async def login(user: User, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=user.email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user