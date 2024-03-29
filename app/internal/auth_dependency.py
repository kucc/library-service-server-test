from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from config import ACCESS_TOKEN_Settings, FB_Settings

from models import User

from database import get_db
from internal.schemas.auth_schema import *
from internal.security import firebasescrypt
from internal.custom_exception import *

fb_settings = FB_Settings()

access_token_setting = ACCESS_TOKEN_Settings()
JWT_SECRET_KEY = access_token_setting.jwt_secret_key
JWT_ALGORITHM = access_token_setting.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3 # 3일

# OAuth2PasswordBearer를 사용하여 Authorization 헤더에서 토큰을 추출
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# oauth_scheme을 사용하기 위한 dependency
def get_oauth2_scheme():
    return oauth2_scheme

# create access token
def create_access_token(user_id: int, email: str, is_admin: bool):
    data = {
        "user_id": user_id,
        "email": email,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    access_token = Token(access_token=token, token_type="bearer")
    return access_token

# verify password
def verify_password(
        plain_password: str, 
        password_hash: str, 
        salt: str,
        salt_separator: str = fb_settings.fb_salt_separator,
        signer_key: str = fb_settings.fb_signer_key,
        rounds: int = fb_settings.fb_rounds,
        mem_cost: int = fb_settings.fb_mem_cost
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

# authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password, user.salt):
        return user
    return None

# decode token
def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(sstatus_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# 사용자 정보 가져오기
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
        ):
    # token을 decode해서 user 정보 가져오기
    user = decode_token(token)
    # db에서 사용자 정보 조회
    db_user = db.query(User).filter(User.email == user["email"]).first()
    # user가 없으면 HTTPException 발생
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
            )
    # user가 맞으면 user 정보 반환
    return user

# 현재 활성화된 사용자 정보 가져오기
async def get_current_active_user(db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    user = db.query(User).filter(User.email == current_user['email']).first()
    # 만약 user의 status가 0이면 HTTPException 발생 (status_code=400, detail="Inactive user")
    if user.status == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    # 만약 user의 valid가 0이면 HTTPException 발생 (status_code=400, detail="Inactive user")
    if user.valid == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    user_info = {
        "user_id": user.user_id,
        "email": user.email,
        "user_name": user.user_name,
        "status": user.status,
        "valid": user.valid
    }

    if user.admin and user.admin.admin_status == True:
        user_info["admin_id"] = user.admin.admin_id
        user_info["admin_status"] = user.admin.admin_status
        current_active_user = AuthUserResponse(user=AuthAdmin(**user_info))
    else:
        current_active_user = AuthUserResponse(user=AuthUser(**user_info))

    # active 상태면 user 정보(current_user) 반환
    return current_active_user