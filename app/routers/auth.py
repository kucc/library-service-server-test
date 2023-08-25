# /auth 경로에 대한 핸들러 함수
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models import User
from config import FB_Settings

# from internal.schemas.auth_dependency_schema import *
# from internal.crudf import *

from internal.schemas.auth_schema import *
from internal.auth_dependency import *

from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
setting = FB_Settings()

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
        user_info["admin_id"] = user.admin.admin_id
        user_info["admin_status"] = user.admin.admin_status
        auth_response = AuthUserResponse(user=AuthAdmin(**user_info))
    else:
        auth_response = AuthUserResponse(user=AuthUser(**user_info))

    print(auth_response)
    return auth_response

# 로그인
    # authenticate user
    # create access token
    # return token

# 회원가입

# 로그아웃

# 비밀번호 변경

# 회원 탈퇴