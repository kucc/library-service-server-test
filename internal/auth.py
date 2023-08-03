### internal/auth.py
import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status, Response
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import User, Admin, Book
from config import Settings
from internal import firebasescrypt

from internal.custom_exception import ItemKeyValidationError, ForeignKeyValidationError
from internal.schema import *
from internal.crudf import *
from internal.salt import *

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
setting = Settings()

salt_separator = setting.fb_salt_separator
signer_key = setting.fb_signer_key
rounds = setting.fb_rounds
mem_cost = setting.fb_mem_cost

# /auth 경로에 대한 핸들러 함수
@router.get("/")
async def get_auths(
        db: Session = Depends(get_db)
):
    auths = db.query(UserIn).all()
    if auths:
        return auths

# 사용자 명으로 모델 객체 리턴
def get_user(email: str, db: Session):
    if email in db.query(User).filter(User.email == email).first():
        return db.query(User).filter(User.email == email).first()

# password 검증
def verify_password(plain_password: str, hashed_password: str):
    return firebasescrypt.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    user = get_user(token, get_db())
    if user is None:
        raise credentials_exception
    return user

@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# 로그인
@router.post("/login",
             status_code=status.HTTP_201_CREATED,
             response_model=Token,
             response_description="Success to login"
             )
async def login(req: UserIn, db: Session = Depends(get_db)):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - username: Unique identifier for a user e.g email, 
                phone number, name

    - password:
    """

    return "token"

# 회원가입
@router.post("/register")
async def register(req: UserIn, db: Session = Depends(get_db)):

    # salt.py 사용해야 함!
    # [8:] 잊지 말 것

    """Creates a new user and returns a token
    on successful creation.

    request body:

    - username: Unique identifier for a user e.g email, 
                phone number, name

    - password:
    """


# 비밀번호 변경
@router.post("/password")
async def change_password(req: UserIn, db: Session = Depends(get_db)):
    """Changes user's password and returns a token
    on successful creation.

    request body:

    - username: Unique identifier for a user e.g email, 
                phone number, name

    - password:
    """

# 로그아웃
@router.post("/logout")
async def logout(req: UserIn, db: Session = Depends(get_db)):
    """Logs out a user and returns a token
    on successful creation.

    request body:

    - username: Unique identifier for a user e.g email, 
                phone number, name

    - password:
    """