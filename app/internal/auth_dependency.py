from datetime import datetime, timedelta
from typing import Annotated, Union

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
SECRET_KEY = access_token_setting.secret_key
ALGORITHM = access_token_setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3 # 3일

# OAuth2PasswordBearer를 사용하여 Authorization 헤더에서 토큰을 추출
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# create access token
def create_access_token(sub: str, email: str, is_admin: bool):
    data = {
        "sub": sub,
        "email": email,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    access_token = Token(token=token, token_type="bearer")
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

# verify access token
def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # decoded_token은 payload
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")



'''





# 엔드포인트 정의


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




# 현재 사용자 정보 가져오기
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # sub: 토큰의 subject. 사용자의 identification을 넣는 곳.
        # JWT는 user를 idenify하는데 사용될뿐 아니라, API에서 바로 동작할 수 있도록 해준다.
        # car, blog post 등을 통해 identify하고, drive, edit 등의 권한을 부여할 수 있다.
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# 현재 활성화된 사용자 정보 가져오기
async def get_current_active_user(
        current_user: Annotated[UserIn, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

'''