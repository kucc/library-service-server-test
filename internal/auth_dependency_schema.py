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