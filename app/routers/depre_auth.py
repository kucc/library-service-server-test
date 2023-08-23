### internal/auth.py

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models import User
from config import FB_Settings

from internal.schemas.auth_dependency_schema import *
from internal.crudf import *

router = APIRouter(prefix="/depre_auth", tags=["depre_auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
setting = FB_Settings()

fb_salt_separator = setting.fb_salt_separator
fb_signer_key = setting.fb_signer_key
fb_rounds = setting.fb_rounds
fb_mem_cost = setting.fb_mem_cost

# /auth 경로에 대한 핸들러 함수
@router.get("")
async def get_auths(
        db: Session = Depends(get_db)
):
    auths = db.query(User).all()
    if auths:
        return auths
    else:
        raise HTTPException(status_code=404, detail="No auths found")

# 로그인
@router.post("/token",
             status_code=status.HTTP_201_CREATED,
             response_model=Token,
             response_description="Success to login"
             )
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    # 추후 authenticate_user()로 뺄지 고민
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 예시
@router.get("/users/me, response_mode=User")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

# 예시
@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


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