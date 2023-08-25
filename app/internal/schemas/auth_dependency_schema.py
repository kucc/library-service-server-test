from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from database import get_db
from internal.schemas.schema import *
from internal.security import firebasescrypt
from internal.custom_exception import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 추후 openssl rand -hex 32로 secret key 생성해서 수정할 예정
# 아래 SECRET_KEY는 임시 키
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 1 # 1일

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from pydantic import BaseModel

app = FastAPI()

# 토큰 생성 및 검증을 위한 키
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# JWT를 검증하기 위한 함수
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# OAuth2PasswordBearer를 사용하여 Authorization 헤더에서 토큰을 추출
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 엔드포인트 정의
@app.get("/{user_id}/profile")
async def get_user_profile(user_id: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload.get("sub") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]

@app.patch("/{user_id}/profile")
async def update_user_profile(user_id: str, profile_update: UserProfile, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload.get("sub") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = profile_update.dict(exclude_unset=True)
    fake_db[user_id].update(update_data)
    return fake_db[user_id]
