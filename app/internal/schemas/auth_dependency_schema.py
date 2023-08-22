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

########## schemas ##########

'''
class UserBase(BaseModel):
    user_id: int
    username: str
    email: str
    status: bool # 활동 여부
    valid: bool # 유효 여부

class User(UserBase):
    is_active: bool = True

class Admin(UserBase):
    admin_id: int = None
    admin_status: bool = False

class UserWithAdmin(UserBase):
    status: bool = True
    valid: bool = True
    admin_id: int = None
    admin_status: bool = True
'''

### Auth - 토큰 정보
class Token(BaseModel):
    access_token: str
    token_type: str

# 토큰에 담을 정보
class TokenData(BaseModel):
    email: Union[str, None] = None

# Auth - 로그인 정보
class UserIn(BaseModel):
    user_id: int
    email: str
    user_name: str
    status: bool # 활동 여부
    valid: bool # 유효 여부

class Admin(BaseModel):
    admin_id: int = None
    admin_status: bool = False

# Password가 맞는지 검사하기 위해 데이터를 이 곳에 먼저 넣음
class UserInDB(UserIn):
    salt: str
    hashed_password: str


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

def get_user(email: str, db: Session = Depends(get_db)):
    user = db.query(UserIn).filter(UserIn.email == email).first()
    return user

#######여기서부터 외부에서도 쓰는 dependecy ########

# 액세스 토큰 생성
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # 1시간
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(   # 이따 확인하고 수정
        to_encode, 
        "secret", 
        algorithm="HS256"
    )
    return encoded_jwt

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