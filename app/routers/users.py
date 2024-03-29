from fastapi import APIRouter, Depends, status
from database import get_db
from internal.schemas.schema import *
from models import *
from internal.crudf import *
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, time, timedelta
import math


router = APIRouter(prefix="/users", tags=["users"])


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
    return get_list_of_item(model=User, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o, init_query=None,
                            db=db)


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
    req: UserIn = Depends(),
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
    db: Session = Depends(get_db)
):
    return get_item_by_column(model=Loan, columns={"user_id": user_id, "return_status": False}, mode=True, db=db)


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
    db: Session = Depends(get_db)
):
    return get_item_by_column(model=BookRequest, columns={"user_id": user_id, "processing_status": 0}, mode=True, db=db)


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
            response_model=BookRequestOut,
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
            response_model=BookRequestOut,
            status_code=status.HTTP_201_CREATED,
            response_description="Success to create the book-request information"
            )
async def create_book_request(
    user_id: int,
    req: BookRequestIn = Depends(),
    db: Session = Depends(get_db)
):
    #req.user_id = user_id
    return create_item(BookRequest, req, db)


# 회원 도서 신청 수정
@router.patch("/{user_id}/book-requests/{book_request_id}",
            status_code=status.HTTP_200_OK,
            response_model=BookRequestOut,
            response_description="Success to patch the user's book-request information",
            response_model_exclude={"valid"}
            )
async def update_book_request(
    user_id: int,
    book_request_id: int,
    req: BookRequestIn = Depends(),
    db: Session = Depends(get_db)
):
    #req.user_id = user_id
    return update_item(model=BookRequest, req=req, index=book_request_id, db=db)


# 회원 도서 신청 삭제
@router.delete("/{user_id}/book-requests/{book_request_id}",
            status_code=status.HTTP_200_OK,
            response_description="Success to delete the user's book-request information"
            )
async def delete_book_request(
    user_id: int,
    book_request_id: int,
    db: Session = Depends(get_db)
):
    return delete_item(model=BookRequest, index=book_request_id, db=db)


# 회원 도서 후기 작성
@router.post("/{user_id}/reviews/{book_info_id}",
            response_model=BookReviewOut,
            status_code=status.HTTP_201_CREATED,
            response_description="Success to create the user's book review"
            )
async def create_book_review(
    user_id: int,
    book_info_id: int,
    req: BookReviewIn = Depends(),
    db: Session = Depends(get_db)
):
    #req.user_id = user_id
    #req.book_info_id = book_info_id
    return create_item(BookReview, req, db)


# 회원 도서 후기 수정
@router.patch("/{user_id}/reviews/{review_id}",
            response_model=BookReviewOut,
            status_code=status.HTTP_201_CREATED,
            response_description="Success to patch the user's book review",
            response_model_exclude={"valid"}
            )
async def update_book_request(
    user_id: int,
    review_id: int,
    req: BookReviewIn = Depends(),
    db: Session = Depends(get_db)
):
    #req.user_id = user_id
    return update_item(model=BookReview, req=req, index=review_id, db=db)


# 회원 도서 후기 삭제
@router.delete("/{user_id}/reviews/{review_id}",
            status_code=status.HTTP_200_OK,
            response_description="Success to delete the user's book review"
            )
async def delete_book_review(
    user_id: int,
    review_id: int,
    db: Session = Depends(get_db)
):
    return delete_item(model=BookReviewIn, index=review_id, db=db)


# 회원 도서 대출
@router.post("/{user_id}/task/loan/{book_id}",
            response_model=LoanOut,
            status_code=status.HTTP_201_CREATED,
            response_description="Success to loan the book",
            response_model_exclude={"valid"}
            )
async def create_loan(
    user_id: int,
    book_id: int,
    req: LoanIn,
    db: Session = Depends(get_db)
):
    req.user_id = user_id
    req.book_id = book_id
    req.loan_date = datetime.now().replace(microsecond=0)
    expected_return_date = req.loan_date + timedelta(days=7)
    req.expected_return_date = datetime.combine(expected_return_date.date(),time.max).replace(microsecond=0)
    return create_item(Loan, req, db)


# 회원 대출별 남은 대출 일자 조회
@router.get("/{user_id}/task/loan/loan-period/{loan_id}",
            status_code=status.HTTP_200_OK,
            response_description="Success to get remaining loan period of the loan"
            )
async def get_user_loan_remaining_period(
    user_id: int,
    loan_id: int,
    db: Session = Depends(get_db)
):
    init_query = db.query(Loan).filter(Loan.user_id == user_id, Loan.loan_id == loan_id).one()
    remaining_period = (init_query.expected_return_date - datetime.now().replace(microsecond=0)).total_seconds() / 86400.0 # 86400초 = 1일
    if remaining_period < 0:
        return "반납 기한을 %d일 초과하였습니다." % int(math.floor(remaining_period))
    else:
        if math.trunc(remaining_period) == 0:
            return "반납 당일입니다! 오후 11시 59분까지 반납하세요."
        return "반납 기한이 %d일 남았습니다." %  math.trunc(remaining_period)


# 회원 도서 대출 연장
@router.patch("/{user_id}/task/extend/{loan_id}",
            status_code=status.HTTP_200_OK,
            response_model=LoanOut,
            response_description="Success to renew the loan",
            response_model_exclude={"valid"}
            )
async def update_renew_loan(
    user_id: int,
    loan_id: int,
    req: LoanExtend,
    db: Session = Depends(get_db)
):
    init_query = db.query(Loan).filter(Loan.user_id == user_id, Loan.loan_id == loan_id).one()
    if init_query.extend_status is True:
        return "You've already extended the loan!"
    else:
        req.extend_status = True
        expected_return_date = init_query.expected_return_date + timedelta(days=8)
        req.expected_return_date = datetime.combine(expected_return_date.date(),time.max).replace(microsecond=0)
        return update_item(model=Loan, req=req, index=loan_id, db=db)


# 회원 도서 대출 반납
@router.patch("/{user_id}/task/return/{loan_id}",
            status_code=status.HTTP_200_OK,
            response_model=LoanOut,
            response_description="Success to return the loan",
            response_model_exclude={"valid"}
            )
async def update_return_loan(
    user_id: int,
    loan_id: int,
    req: LoanReturn,
    db: Session = Depends(get_db)
):
    init_query = db.query(Loan).filter(Loan.user_id == user_id, Loan.loan_id == loan_id).one()
    if init_query.return_status is True:
        return "You've already returned the book!"
    else:
        req.return_status = True
        req.return_date = datetime.now().replace(microsecond=0)
        delay_days = (req.return_date - init_query.expected_return_date).total_seconds() / 86400.0
        if delay_days > 0:
            req.delay_days = math.ceil(delay_days)
        return update_item(model=Loan, req=req, index=loan_id, db=db)