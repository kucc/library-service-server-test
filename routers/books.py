#
from fastapi import APIRouter, Query, status
from typing import Optional
from database import Engineconn
from models import *
from datetime import datetime, timedelta

engine = Engineconn()
session = engine.sessionmaker()
router = APIRouter(prefix="/books", tags=["books"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

# /books 경로에 대한 핸들러 함수
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
        query = query.filter(BookInfo.author == author)
    if publication_year is not None and not isinstance(author, str):
        query = query.filter(BookInfo.publication_year == publication_year)
    if category_id is not None and not isinstance(author, int):
        query = query.filter(BookInfo.category_id == category_id)
    if publisher is not None and not isinstance(author, str):
        query = query.filter(BookInfo.publisher == publisher)
    if title is not None and not isinstance(author, str):
        query = query.filter(BookInfo.title.contains(title))
    if major is not None and not isinstance(author, bool):
        query = query.filter(BookInfo.title)

    #---------------------Query Parameter를 통한 필터링!---------------------------
    query = session.query(BookInfo)
    if author 

    
    if get_begin:
        try:
            query = query.filter(BookInfo.updated_at >= get_begin)
        except ValueError:
            return {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid get_begin format. It should be in YYYY-MM-DD format.",
            }
    else:
        get_begin = datetime.today() - timedelta(days=30)
        query = query.filter(BookInfo.updated_at >= get_begin)
    if get_end:
        try:
            query = query.filter(BookInfo.updated_at <= get_end)
        except ValueError:
            return {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid get_end format. It should be in YYYY-MM-DD format.",
            }
    else:
        get_end = datetime.today()
        query = query.filter(BookInfo.updated_at <= get_end)
    #------------------------------------------------------------------------------
    books_info = query.all()
    
    if books_info:
        return {
            "code": status.HTTP_200_OK,
            "message": "success to get book information",
            "result": books_info
        }
    else:
        return {
            "code": status.HTTP_204_NOT_FOUND,
            "message": "fail to get book information"
        }
    
@router.get("/{book_info_id}")
def get_query(
    book_info_id: int,
    ):

    book_info_id = session.query(BookInfo).filter(BookInfo.query_id == query_id).one()
    if book_info_id:
        return {
            "code": status.HTTP_200_OK,
            "message": "success to get book information",
            "result": query
        }
    else:
        return {
            "code": status.HTTP_404_NOT_FOUND,
            "message": "fail to get book information"
        }

@router.get("/")
