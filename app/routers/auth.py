# /auth 경로에 대한 핸들러 함수
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import User
from config import FB_Settings

from typing import Annotated

from internal.schemas.auth_schema import *
from internal.auth_dependency import *

from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
setting = FB_Settings()

# /auth 핸들러 함수
@router.get("/")
async def get_auth():
    return {"message": "Hello, World!"}

# 테스트
# 일반 사용자: mjkweon17@korea.ac.kr
# 관리자: thisisfortest@gmail.com
@router.get("/{email}", response_model=AuthUserResponse, status_code=status.HTTP_200_OK, response_description="Get user info")
async def get_user(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_info = {
        "user_id": user.user_id,
        "email": user.email,
        "user_name": user.user_name,
        "status": user.status,
        "valid": user.valid
    }

    if user.admin:
        user_info["access_token"] = create_access_token(user.user_id, user.email, True)
        user_info["admin_id"] = user.admin.admin_id
        user_info["admin_status"] = user.admin.admin_status
        auth_response = AuthUserResponse(user=AuthAdmin(**user_info))
    else:
        user_info["access_token"] = create_access_token(user.user_id, user.email, False)
        auth_response = AuthUserResponse(user=AuthUser(**user_info))

    #auth_response.user.access_token = Token(token="123", token_type="bearer")

    return auth_response

# 로그인
'''
@router.post("/token",
             status_code=status.HTTP_201_CREATED,
             response_model=Token,
             response_description="Success to login"
             )
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    return "dtd"
'''


'''
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    # authenticate user
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.password, user.salt, fb_salt_separator, fb_signer_key, fb_rounds, fb_mem_cost):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )  
    # create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # return token
    return {"access_token": access_token, "token_type": "bearer"}
'''

# 회원가입

# 로그아웃

# 비밀번호 변경

# 회원 탈퇴