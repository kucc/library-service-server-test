from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from config import ACCESS_TOKEN_Settings

from database import get_db
from internal.schemas.auth_schema import *
from internal.security import firebasescrypt
from internal.custom_exception import *

setting = ACCESS_TOKEN_Settings()
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3 # 3일

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



'''

# authenticate user

# verify password
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

# 비밀번호 해싱
def get_hashed_password():
    pass

def get_user(email: str, db: Session = Depends(get_db)):
    user = db.query(UserIn).filter(UserIn.email == email).first()
    return user

# create access token


# verify access token

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