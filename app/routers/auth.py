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
@router.get("/{email}", response_model=AuthUserResponse, status_code=status.HTTP_200_OK, response_description="테스트 API")
async def get_user_for_test(email: str, db: Session = Depends(get_db)):
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

    return auth_response

# 로그인
@router.post("/token",
             response_model=AuthUserResponse,
             status_code=status.HTTP_201_CREATED,
             response_description="Success to login"
             )
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise CredentialsException()

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

    return auth_response


# 회원가입

# 로그아웃

# 비밀번호 변경

# 회원 탈퇴



'''

# 회원가입
@router.post("/register")
async def register(req: UserIn, db: Session = Depends(get_db)):

    # ★★★★★ 테스트 중 ★★★★★

    # salt.py 사용해야 함!
    # [8:] 잊지 말 것

    # 현재 테스트 중인 부분
        # firebase에 회원가입하면 random으로 개인 고유의 salt 생성됨
        # firebase의 salt 생성법은 공개되지 않음
        # 최대한 비슷한 방식으로 

    """Creates a new user and returns a token
    firebase에 성공적으로 회원가입되면 그때 실행될 API

    on successful creation.

    request body:
    - email: Unique identifier for a user
    - username: real name
    - password:

    return token
    """

# 로그아웃
@router.post("/logout")
async def logout(req: UserIn, db: Session = Depends(get_db)):
    return {"message": "Logout successfully"}

# 비밀번호 변경
@router.post("/password")
async def change_password(req: UserIn, db: Session = Depends(get_db)):
    """Changes user's password and returns a token
    on successful creation.

    not implemented yet

    request body:

    """

# 회원 탈퇴
@router.delete("/delete")
async def delete_user(req: UserIn, db: Session = Depends(get_db)):
    """Deletes user's account
    
    not implemented yet

    request body:

    """


'''