#
from fastapi import APIRouter, Query, status
from typing import Optional
from database import Engineconn
from models import *
from datetime import datetime, timedelta

engine = Engineconn()
session = engine.sessionmaker()
router = APIRouter(prefix="/books", tags=["books"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

# /books 경로에 대한 핸들러 함수 (전체 도서 정보 조회)
@router.get("/")
def get_books(
    author: Optional[int] = None,
    publication_year: Optional[int] = None,
    category_id: Optional[int] = None,
    publisher: Optional[str] = None,
    title: Optional[str] = None,
    major: Optional[bool] = None,

    get_begin: Optional[str] = None,
    get_end: Optional[str] = None
):
    
    # Query Parameter (get_begin, get_end 제외) Validation
    if author is not None and not isinstance(author, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid author name",
        }
    if publication_year is not None and not isinstance(publication_year, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid author name",
        }
    if category_id is not None and not isinstance(category_id, int):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid category id",
        }
    if publisher is not None and not isinstance(publisher, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid publisher name",
        }
    if title is not None and not isinstance(title, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid title name",
        }
    if major is not None and not isinstance(major, bool):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid major status",
        }

    #---------------------Query Parameter를 통한 필터링!---------------------------
    query = session.query(BookInfo)
    if author:
        query = query.filter(BookInfo.author.contains(author))
    if publication_year:
        query = query.filter(BookInfo.publication_year == publication_year)
    if category_id:
        query = query.filter(BookInfo.category_id == category_id)
    if publisher:
        query = query.filter(BookInfo.publisher == publisher)
    if title:
        query = query.filter(BookInfo.title.contains(title))
    if major:
        query = query.filter(BookInfo.major is True)
    
    if get_begin:
        try:
            begin_date = datetime.strptime(get_begin, "%Y-%m-%d")
            query = query.filter(BookInfo.updated_at >= begin_date)
        except ValueError:
            return {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid begin_date format. It should be in YYYY-MM-DD format.",
            }

    if get_end:
        try:
            end_date = datetime.strptime(get_end, "%Y-%m-%d")
            query = query.filter(BookInfo.updated_at <= get_end)
        except ValueError:
            return {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid get_end format. It should be in YYYY-MM-DD format.",
            }
    
    #---------------------딕셔너리(결과값) 반환---------------------------
    books_info = query.all()
    
    if books_info:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success to get book information",
            "result": books_info
        }
    else:
        return {
            "code": status.HTTP_204_NOT_FOUND,
            "message": "Fail to get book information",
            "result": []
        }

# 개별 도서 정보 조회
@router.get("/{book_info_id}")
def get_book(
    book_info_id: int
    ):

    book_info = session.query(BookInfo).filter(BookInfo.book_info_id == book_info_id).one()
    if book_info:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success to get book information",
            "result": book_info
        }
    else:
        return {
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Fail to get book information"
        }

@router.get("/{book_info_id}/book-holding")
def get_book_holding(
    book_info_id: int
    ):
    book_holding = session.query(Book).filter(Book.book_info_id == book_info_id).all()
    if book_holding:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success to get book holding information",
            "result": book_holding
        }
    else:
        return {
            "code": status.HTTP_204_NOT_FOUND,
            "message": "Fail to get book holding information",
            "result": book_holding
        }
