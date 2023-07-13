from fastapi import APIRouter, Query, status
from typing import Optional
from database import Engineconn
from models import Book, BookInfo, BookReview, BookRequest
from datetime import datetime, timedelta


engine = Engineconn()
session = engine.sessionmaker()
router = APIRouter(prefix="/books", tags=["books"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})


# /books 경로에 대한 핸들러 함수 (전체 도서 정보 조회)
@router.get("")
def get_books(
    author: Optional[str] = None,
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
            "message": "Invalid author name"
        }
    if publication_year is not None and not isinstance(publication_year, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid author name"
        }
    if category_id is not None and not isinstance(category_id, int):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid category id"
        }
    if publisher is not None and not isinstance(publisher, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid publisher name"
        }
    if title is not None and not isinstance(title, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid title name"
        }
    if major is not None and not isinstance(major, bool):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid major status"
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
                "message": "Invalid begin_date format. It should be in YYYY-MM-DD format."
            }

    if get_end:
        try:
            end_date = datetime.strptime(get_end, "%Y-%m-%d")
            query = query.filter(BookInfo.updated_at <= get_end)
        except ValueError:
            return {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid end_date format. It should be in YYYY-MM-DD format."
            }
    
    #---------------------딕셔너리(결과값) 반환---------------------------
    books_info = query.all()
    
    if books_info is None:
        return {
            "code": status.HTTP_204_NO_CONTENT,
            "message": "In the request was successfully processed, but there is NoneType object.",
            "result": []
        }
    else:
        if books_info:
            return {
                "code": status.HTTP_200_OK,
                "message": "Success to get book information",
                "result": books_info
            }
        else:
            return {
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Fail to get book information",
                "result": []
            }


# 개별 도서 정보 조회
@router.get("/{book_info_id}")
def get_book(
    book_info_id: int
    ):
    book_info = session.query(BookInfo).filter(BookInfo.book_info_id == book_info_id).one()
    if book_info is None:
        return {
            "code": status.HTTP_204_NO_CONTENT,
            "message": "In the request was successfully processed, but there is NoneType object.",
            "result": []
        }
    else:
        if book_info:
            return {
                "code": status.HTTP_200_OK,
                "message": "Success to get book information",
                "result": book_info
            }
        else:
            return {
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Fail to get book information"
            }


# 전체 소장 정보 목록 조회
@router.get("/book-holdings")
def get_book_holdings_all(
        book_info_id: Optional[int] = None,
        donor_name: Optional[str] = None,
        book_status: Optional[int] = None,

        get_begin: Optional[str] = None,
        get_end: Optional[str] = None
    ):

    # Query Parameter (get_begin, get_end 제외) Validation
    if book_info_id is not None and not isinstance(book_info_id, int):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid book information ID"
        }
    if donor_name is not None and not isinstance(donor_name, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid donor name"
        }
    if book_status is not None and not isinstance(book_status, int):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid book status"
        }

    #---------------------Query Parameter를 통한 필터링!---------------------------
    query = session.query(Book)
    if book_info_id:
        query = query.filter(Book.book_info_id == book_info_id)
    if donor_name:
        query = query.filter(Book.donor_name.contatins(donor_name))
    if book_status:
        query = query.filter(Book.book_status == book_status)
    
    if get_begin:
        try:
            begin_date = datetime.strptime(get_begin, "%Y-%m-%d")
            query = query.filter(Book.updated_at >= begin_date)
        except ValueError:
            return {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid begin_date format. It should be in YYYY-MM-DD format."
            }

    if get_end:
        try:
            end_date = datetime.strptime(get_end, "%Y-%m-%d")
            query = query.filter(Book.updated_at <= get_end)
        except ValueError:
            return {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid end_date format. It should be in YYYY-MM-DD format."
            }
    
    #---------------------딕셔너리(결과값) 반환---------------------------
    book_holdings_all = query.all()
    if book_holdings_all is None:
        return {
            "code": status.HTTP_204_NO_CONTENT,
            "message": "In the request was successfully processed, but there is NoneType object.",
            "result": []
        }
    else:
        if book_holdings_all:
            return {
                "code": status.HTTP_200_OK,
                "message": "Success to get whole book-holding informations",
                "result": book_holdings_all
            }
        else:
            return {
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Fail to get whole book-holding informations",
                "result": []
            }


# 개별 소장 정보 목록 조회
@router.get("/book-holdings/{book_id}")
def get_book_holdings(book_id: int):
    book_holdings = session.query(Book).filter(Book.book_id == book_id).one()
    if book_holdings is None:
        return {
            "code": status.HTTP_204_NO_CONTENT,
            "message": "In the request was successfully processed, but there is NoneType object.",
            "result": []
        }
    else:
        if book_holdings:
            return {
                "code": status.HTTP_200_OK,
                "message": "Success to get book-holding information",
                "result": book_holdings
            }
        else:
            return {
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Fail to get book-holding information"
            }
    

# 도서 후기
@router.get("/{book_info_id}/reviews")
def get_book_review(
    book_info_id: int
    ):
    book_reviews = session.query(BookReview).filter(BookReview.book_info_id == book_info_id).all()
    if book_reviews is None:
        return {
            "code": status.HTTP_204_NO_CONTENT,
            "message": "In the request was successfully processed, but there is NoneType object.",
            "result": []
        }
    else:
        if book_reviews:
            return {
                "code": status.HTTP_200_OK,
                "message": "Success to get book information",
                "result": book_reviews
            }
        else:
            return {
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Fail to get book information"
            }
        

#