from fastapi import APIRouter, Depends
from starlette import status
from app.database import get_db
from app.internal.schemas.schema import BookHoldOut, BookReviewOut, BookInfoOut, \
    BookInfoQuery,BookReviewQuery,BookHoldQuery,BookInfoByID
from app.models import Book, BookInfo, BookReview
from app.internal.crudf import *
from sqlalchemy.orm import Session, joinedload

router = APIRouter(prefix="/books", tags=["books"])


# /books 핸들러 함수 (전체 도서 정보 조회)
@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[BookInfoOut],
            response_description="Success to get all book-info information list"
            )
async def get_book_list(
        skip: int | None = 0,
        limit: int | None = 10,
        q: BookInfoQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        db: Session = Depends(get_db)
):
    return get_list_of_item(model=BookInfo, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o, init_query=None,
                            db=db)


# 개별 도서 정보 조회
@router.get("/book-info/{book_info_id}",
            response_model=BookInfoByID,
            response_description="Success to get the book-info information"
            )
async def get_book_info(
        book_info_id: int,
        db: Session = Depends(get_db)
):
    query = db.query(BookInfo).options(joinedload(BookInfo.books))
    book_info = query.filter(BookInfo.book_info_id == book_info_id).first()
    if book_info:
        return book_info
    else:
        raise ItemKeyValidationError(detail=("book_info_id", book_info_id))


# 전체 소장 정보 목록 조회
@router.get("/book-holdings",
            status_code=status.HTTP_200_OK,
            response_model=List[BookHoldOut],
            response_description="Success to get all book-holding information list"
            )
async def get_book_holding_list(
        skip: int | None = 0,
        limit: int | None = 10,
        q: BookHoldQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        db: Session = Depends(get_db)
):
    return get_list_of_item(model=Book, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o, init_query=None, db=db)


# 개별 소장 정보 목록 조회
@router.get("/book-holdings/{book_id}",
            status_code=status.HTTP_200_OK,
            response_model=BookHoldOut,
            response_description="Success to get the book-holding information"
            )
async def get_book_holding(
        book_id: int,
        db: Session = Depends(get_db)
):
    return get_item_by_id(model=Book, index=book_id, db=db, user_mode=True)


# 전체 후기 조회
@router.get("/reviews",
            status_code=status.HTTP_200_OK,
            response_model=List[BookReviewOut],
            response_description="Success to get all book-review lists"
            )
async def get_review_list(
        skip: int | None = 0,
        limit: int | None = 10,
        q: BookReviewQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        db: Session = Depends(get_db)
):
    return get_list_of_item(model=BookReview, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o, init_query=None,
                            db=db)


# 특정 도서 후기 조회
@router.get("/{book_info_id}/reviews",
            status_code=status.HTTP_200_OK,
            response_model=List[BookReviewOut],
            response_description="Success to get all book-review lists"
            )
async def get_book_review_list(
        book_info_id: int,
        skip: int | None = 0,
        limit: int | None = 10,
        q: BookReviewQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        db: Session = Depends(get_db)
):
    init_query = get_item_by_column(model=BookReview, columns={"book_info_id": book_info_id}, mode=False, db=db)
    return get_list_of_item(model=BookReview, skip=skip, limit=limit, user_mode=True, q=q, p=p, o=o,
                            init_query=init_query, db=db)


# 개별 후기 조회
@router.get("/reviews/{review_id}",
            status_code=status.HTTP_200_OK,
            response_model=BookReviewOut,
            response_description="Success to get the book-review information"
            )
async def get_review(
        review_id: int,
        db: Session = Depends(get_db)
):
    return get_item_by_id(model=BookReview, index=review_id, db=db, user_mode=True)