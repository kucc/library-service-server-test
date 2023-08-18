from fastapi import APIRouter, Depends, status
from database import get_db
from internal.schemas.schema import *
from models import *
from internal.crudf import *
from sqlalchemy.orm import Session, joinedload


router = APIRouter(prefix="/users", tags=["users"])#(prefix="/users", tags=["users"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

# TODO - 완성 시까지
#  1. USERS에서 user_mode는 싹 다 True로 할 것
#  2. response_model_exclude={"valid"} 모두 추가
#  3. loan date는 프론트에서 입력, expected return date와 delay_days는 백엔드에서 계산

# /users 핸들러 함수 (전체 회원 정보 조회)
@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[UserOut],
            response_description="Success to get all users information list",
            response_model_exclude={"valid"}
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
            response_description="Success to get the user information",
            response_model_exclude={"valid"}
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
            response_description="Success to patch the user information",
            response_model_exclude={"valid"}
            )
async def update_user_info(
    user_id: int,
    req: UserIn,
    db: Session = Depends(get_db)
):
    return update_item(model=User, req=req, index=user_id, db=db)


# 회원 현재 대출 목록 조회
@router.get("/{user_id}/loans/current",
            status_code=status.HTTP_200_OK,
            response_model=List[LoanOut],
            response_description="Success to get the user's current loan information",
            response_model_exclude={"valid"}
            )
async def get_user_current_loan_list(
    user_id: int,
    skip: int | None = 0,
    limit: int | None = 10,
    q: LoanQuery = Depends(),
    p: PeriodQuery = Depends(),
    o: OrderBy = Depends(),
    db: Session = Depends(get_db)
):
    init_query = get_item_by_column(model=Loan, columns={"user_id": user_id, "return_status": False}, mode=False, db=db)
    return get_list_of_item(model=Loan, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o,
                            init_query=init_query, db=db)


# 회원 전체 기간 대출 목록 조회
@router.get("/{user_id}/loans",
            status_code=status.HTTP_200_OK,
            response_model=List[LoanOut],
            response_description="Success to get the user's all loan informations",
            response_model_exclude={"valid"}
            )
async def get_user_loan_list(
    user_id: int,
    skip: int | None = 0,
    limit: int | None = 10,
    q: LoanQuery = Depends(),
    p: PeriodQuery = Depends(),
    o: OrderBy = Depends(),
    db: Session = Depends(get_db)
):
    init_query = get_item_by_column(model=Loan, columns={"user_id": user_id}, mode=False, db=db)
    return get_list_of_item(model=Loan, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o,
                            init_query=init_query, db=db)


# 회원 전체 기간 후기 조회
@router.get("/{user_id}/reviews",
            status_code=status.HTTP_200_OK,
            response_model=List[BookReviewOut],
            response_description="Success to get the user's all reviews",
            response_model_exclude={"valid"}
            )
async def get_user_review_list(
    user_id: int,
    skip: int | None = 0,
    limit: int | None = 10,
    q: BookReviewQuery = Depends(),
    p: PeriodQuery = Depends(),
    o: OrderBy = Depends(),
    db: Session = Depends(get_db)
):
    init_query = get_item_by_column(model=BookReview, columns={"user_id": user_id}, mode=False, db=db)
    return get_list_of_item(model=BookReview, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o,
                            init_query=init_query, db=db)


# 회원 현재 도서 신청 목록 조회
@router.get("/{user_id}/book-requests/current",
            status_code=status.HTTP_200_OK,
            response_model=List[BookRequestOut],
            response_description="Success to get the user's current book-requests",
            response_model_exclude={"valid"}
            )
async def get_user_current_book_request_list(
    user_id: int,
    skip: int | None = 0,
    limit: int | None = 10,
    q: BookRequestQuery = Depends(),
    p: PeriodQuery = Depends(),
    o: OrderBy = Depends(),
    db: Session = Depends(get_db)
):
    init_query = get_item_by_column(model=BookRequest, columns={"user_id": user_id, "processing_status": 0}, mode=False, db=db)
    return get_list_of_item(model=BookRequest, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o,
                            init_query=init_query, db=db)


# 회원 전체 기간 도서 신청 목록 조회
@router.get("/{user_id}/book-requests",
            status_code=status.HTTP_200_OK,
            response_model=List[BookRequestOut],
            response_description="Success to get the user's all book-requests",
            response_model_exclude={"valid"}
            )
async def get_user_book_request_list(
    user_id: int,
    skip: int | None = 0,
    limit: int | None = 10,
    q: BookRequestQuery = Depends(),
    p: PeriodQuery = Depends(),
    o: OrderBy = Depends(),
    db: Session = Depends(get_db)
):
    init_query = get_item_by_column(model=BookRequest, columns={"user_id": user_id}, mode=False, db=db)
    return get_list_of_item(model=BookRequest, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o,
                            init_query=init_query, db=db)


# 특정 도서 신청 정보 조회
@router.get("/book-requests/{book_request_id}",
            status_code=status.HTTP_200_OK,
            response_model=List[BookRequestOut],
            response_description="Success to get the book-request information",
            response_model_exclude={"valid"}
            )
async def get_user_book_request_list(
    book_request_id: int,
    db: Session = Depends(get_db)
):
    return get_item_by_id(model=BookRequest, index=book_request_id, db=db, user_mode=True)


# 회원 도서 신청
@router.post("/{user_id}/book-requests",
            response_model=List[BookRequestOut],
            status_code=status.HTTP_201_CREATED,
            response_description="Success to create the book-request information"
            )
async def create_book_request(
    user_id: int,
    req: BookRequestIn,
    db: Session = Depends(get_db)
    ):
    return create_item(BookRequest, req, db)


# 회원 도서 신청 수정
@router.patch("/{user_id}/book-requests/{book_request_id}",
            status_code=status.HTTP_200_OK,
            response_model=List[BookRequestOut],
            response_description="Success to patch the user's book-request information",
            response_model_exclude={"valid"}
            )
async def update_book_request(
    user_id: int,
    book_request_id: int,
    req: BookRequestIn,
    db: Session = Depends(get_db)
):
    return update_item(model=BookRequest, req=req, index=book_request_id, db=db)


