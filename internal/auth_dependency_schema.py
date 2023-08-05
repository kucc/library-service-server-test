from datetime import datetime, timedelta
from typing import Annotated, Union, Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import jwt

from database import get_db

from internal import firebasescrypt


########## schema ##########

# Auth - 로그인 정보
class UserIn(BaseModel):
    user_id: int
    user_name: str
    status: bool
    email: str
    valid: bool

# Password가 맞는지 검사하기 위해 데이터를 이 곳에 먼저 넣음
class UserInDB(UserIn):
    salt: str
    hashed_password: str

### Auth - 토큰 정보
class Token(BaseModel):
    access_token: str
    token_type: str

########## dependency ##########

# 비밀번호 해싱
def get_hashed_password():
    pass

# 비밀번호 검증
def verify_password(
        plain_password: str, 
        password_hash: str, 
        salt: str,
        salt_separator: str,
        signer_key: str,
        rounds: int,
        mem_cost: int
        ) -> bool:
    is_valid = firebasescrypt.verify_password(
        password=plain_password,
        known_hash=password_hash,
        salt=salt,
        salt_separator=salt_separator,
        signer_key=signer_key,
        rounds=rounds,
        mem_cost=mem_cost
    )
    return is_valid








"""

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

"""

"""
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

"""