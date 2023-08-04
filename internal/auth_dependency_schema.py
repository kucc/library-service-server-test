from typing import Annotated, Union, Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, validator
# from typing import List
# from internal.custom_exception import InvalidDateFormatError
import os
from datetime import datetime, timedelta
from jose import jwt
from database import get_db
from sqlalchemy.orm import Session
from internal import firebasescrypt


oauth2scheme = OAuth2PasswordBearer(tokenUrl="token")

########## schema ##########

# Auth - 로그인 정보

class UserIn(BaseModel):
    email: str

class UserInDB(UserIn):
    password: str

### Auth - 토큰 정보
class Token(BaseModel):
    access_token: str
    token_type: str
    email: str

class User(BaseModel):
    username: str   # email과 동일?
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

########## dependency ##########

# https://essenceofinvesting.tistory.com/114

# 비밀번호 해싱
def get_hashed_password(password: str) -> str:
    salt = "salt"
    hashed_password = salt + password
    return hashed_password

# 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return firebasescrypt.verify(plain_password, hashed_password)

# 사용법: https://essenceofinvesting.tistory.com/114
# 공식 문서: https://pypi.org/project/python-jose/
ACCESS_TOKEN_EXPIRE_MINUTES = 30    # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECREt_key = os.environ.get("JWT_REFRESH_SECRET_KEY")

# 토큰 생성
def create_access_token(data: dict, expires_delta: datetime.timedelta = datetime.timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 리프레시 토큰 생성
def create_refresh_token(data: dict, expires_delta: datetime.timedelta = datetime.timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECREt_key, algorithm=ALGORITHM)
    return encoded_jwt

# 토큰 디코딩
def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

# DB에서 사용자 정보 검색
def get_user(token: str, db: Session):
    if token in db.query(User).filter(User.email == token).first():
        return db.query(User).filter(User.email == token).first()

def get_user(email: str, db: Session):
    if email in db.query(User).filter(User.email == email).first():
        return db.query(User).filter(User.email == email).first()

# 토큰 검증
async def get_current_user(token: str = Depends(oauth2scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    user = get_user(token, get_db())
    if user is None:
        raise credentials_exception
    return user