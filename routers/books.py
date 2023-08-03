from fastapi import APIRouter, Depends, Query, status, HTTPException
from typing import Optional
from database import get_db
from internal.custom_exception import ItemKeyValidationError, ForeignKeyValidationError, InvalidDateFormatError
from internal.schema import *
from internal.crudf import *
from models import Book, BookInfo, BookReview, BookRequest
from datetime import datetime, timedelta
from sqlalchemy import asc, desc  # asc: 오름차순, desc: 내림차순
from sqlalchemy.orm import Session, joinedload

router = APIRouter(prefix="/books", tags=["books"])


# /books 경로에 대한 핸들러 함수 (전체 도서 정보 조회)
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
    query = get_list_of_item
    query = db.query(BookInfo)
    query = filters_by_query(query, BookInfo, q)
    query = filter_by_period(query, BookInfo, p)
    query = orders_by_query(query, BookInfo, o)
    book_info_list = query.all()

    if book_info_list:
        return book_info_list[skip: skip + limit]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


# 개별 도서 정보 조회
@router.get("/book-info/{book_info_id}",
            status_code=status.HTTP_200_OK,
            response_model=BookInfoByID,
            response_description="Success to get the book-info information"
            )
async def get_book(
        book_info_id: int,
        db: Session = Depends(get_db)
):
    query = db.query(BookInfo).options(joinedload(BookInfo.books)).filter(BookInfo.book_info_id == book_info_id)
    book_info = query.one()

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
    '''
    query = db.query(Book)
    query = filters_by_query(query, Book, q)
    query = filter_by_period(query, Book, p)
    query = orders_by_query(query, Book, o)
    book_holding_list = query.all()

    if book_holding_list:
        return book_holding_list[skip: skip + limit]
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")
    '''
    return get_list_of_item(Book, skip, limit, False, q, p, o, db)


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
    '''
    query = db.query(Book).filter(Book.book_id == book_id)
    book_holding = query.one()

    if book_holding:
        return book_holding
    else:
        raise ItemKeyValidationError(detail=("book_id", book_id))
    '''
    return get_item_by_id(Book, book_id, db)


# 전체 도서 후기 조회
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
    # '''
    # query = db.query(BookReview)
    # query = filters_by_query(query, BookReview, q)
    # query = filter_by_period(query, BookReview, p)
    # query = orders_by_query(query, BookReview, o)
    # book_review_list = query.all()
    #
    # if book_review_list:
    #     return book_review_list[skip: skip + limit]
    # else:
    #     raise ItemKeyValidationError(detail=("book_info_id", book_info_id))
    # '''
    model = BookReview
    use_update_at = False
    return get_list_by_id_query(model, 'book_info_id', book_info_id, skip, limit, use_update_at, q, p, o, db)
    # query = db.query(model).filter_by(book_info_id = book_info_id)
    # query = filters_by_query(query, model, q)
    # query = filter_by_period(query, model, p, use_update_at)
    # query = query.filter(model.valid)
    # query = orders_by_query(query, model, o)
    # result = query.offset(skip).limit(limit).all()
    # if not result:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    #
    # return result


# 개별 도서 후기 조회
@router.get("/reviews/{review_id}",
            status_code=status.HTTP_200_OK,
            response_model=BookReviewOut,
            response_description="Success to get the book-review information"
            )
async def get_book_review(
        review_id: int,
        db: Session = Depends(get_db)
):
    '''
    query = db.query(BookReview).filter(BookReview.review_id == review_id)
    book_review = query.one()

    if book_review:
        return book_review
    else:
        raise ItemKeyValidationError(detail=("review_id", review_id))
    '''
    return get_item_by_id(BookReview, review_id, db)
