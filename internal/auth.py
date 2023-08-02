### internal\auth.py
from typing import Annotated

from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import User, Admin

from config import Settings
import secrets

settings = Settings()
router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenURL="token")

class User(BaseModel):
    email: str
    password: str
    salt: str | None

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

# 회원가입
@router.post("/register")
async def register(user: User, db: Session = Depends(get_db)):
    user = User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 사용자 데이터를 가정한 간단한 데이터베이스
fake_users_db = {
    "user1": {
        "email": "user1",
        "password": "password1"
    },
    "user2": {
        "email": "user2",
        "password": "password2"
    }
}

# 사용자 로그인을 확인하는 의존성 함수
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = fake_users_db.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user    

# 로그아웃
@router.post("/logout")
async def logout(credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(credentials)
    return {"token": credentials, "message": "logout success"}