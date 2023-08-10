from fastapi import APIRouter, Depends, status
from database import get_db
from internal.schemas.schema import *
from models import *
from internal.crudf import *
from sqlalchemy.orm import Session, joinedload


router = APIRouter(prefix="/users", tags=["users"])#(prefix="/users", tags=["users"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})


# /users 핸들러 함수 (전체 회원 정보 조회)
@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[UserOut],
            response_description="Success to get all users information list"
            )
async def get_user_info_list(
        skip: int | None = 0,
        limit: int | None = 10,
        q: UserQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        db: Session = Depends(get_db)
):
    return get_list_of_item(model=User, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o, init_query=None, db=db)


# 개별 회원 정보 조회
@router.get("/{user_id}/profile",
            status_code=status.HTTP_200_OK,
            response_model=UserOut,
            response_description="Success to get the user information"
            )
async def get_user_info(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_item_by_id(model=User, index=user_id, db=db, user_mode=True)


# 회원 정보 수정
@router.patch("/{user_id}/profile",
            status_code=status.HTTP_200_OK,
            response_model=UserOut,
            response_description="Success to patch the user information"
            )
async def update_user_info(
    user_id: int,
    req: UserIn,
    db: Session = Depends(get_db)
):
    return update_item(model=User, req=req, index=user_id, db=db)


# 현재 자기 대출 목록 조회
@router.get("/{user_id}/loans",
            status_code=status.HTTP_200_OK,
            response_model=UserOut,
            response_description="Success to get the user's current loan information"
            )
async def update_user_info(
    user_id: int,
    req: UserIn,
    db: Session = Depends(get_db)
):