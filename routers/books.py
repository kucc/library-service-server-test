from fastapi import APIRouter, Query, status, HTTPException
from typing import Optional
from database import Engineconn
from models import Book, BookInfo, BookReview, BookRequest
from datetime import datetime, timedelta
from sqlalchemy import asc, desc # asc: 오름차순, desc: 내림차순


engine = Engineconn()
session = engine.sessionmaker()
router = APIRouter(prefix="/books", tags=["books"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})


# /books 경로에 대한 핸들러 함수 (전체 도서 정보 조회)
@router.get("")
def get_book_list(
    author: Optional[str] = None,
    publication_year: Optional[int] = None,
    category: Optional[int] = None,
    publisher: Optional[str] = None,
    title: Optional[str] = None,

    only_major: Optional[bool] = False, # 전공도서 여부, 컴퓨터학과 전공도서 조회
    # 정렬 순서를 정하는 세 가지 Query Parameters, 모두 False일 경우 default는 title의 오름차순으로 정렬된다 - 20230716
    by_created_at: Optional[bool] = False, # 최신순, 신착도서 조회
    by_rating: Optional[bool] = False, # 평점순, 인기도서 조회
    by_publication_year: Optional[bool] = False, # 출판순

    get_begin: Optional[str] = None,
    get_end: Optional[str] = None
):
    
    # Query Parameter (get_begin, get_end 제외) Validation
    if author is not None and not isinstance(author, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid author name"
        }
    if publication_year is not None and not isinstance(publication_year, int):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid author name"
        }
    if category is not None and not isinstance(category, int):
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
    
    if only_major is not None and not isinstance(only_major, bool):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid major status"
        }
    if by_created_at is not None and not isinstance(by_created_at, bool) or \
        by_rating is not None and not isinstance(by_rating, bool) or \
        by_publication_year is not None and not isinstance(by_publication_year, bool):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid order status among by_created_at, by_rating, and by_publication_year"
        }

    #---------------------Query Parameter를 통한 필터링!---------------------------
    query = session.query(BookInfo)
    
    if author:
        query = query.filter(BookInfo.author.contains(author))
    if publication_year:
        query = query.filter(BookInfo.publication_year == publication_year)
    if category:
        query = query.filter(BookInfo.category_id == category)
    if publisher:
        query = query.filter(BookInfo.publisher == publisher)
    if title:
        query = query.filter(BookInfo.title.contains(title))
    
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

    # 컴퓨터학과 전공도서, 신착도서, 인기도서, 출판순 검색
    if only_major:
        query = query.filter(BookInfo.major is True)
    if by_created_at:
        if by_rating:
            if by_publication_year:
                query = query.order_by(BookInfo.title.asc(), BookInfo.created_at.desc(), BookInfo.rating.desc(), BookInfo.publication_year.desc())
            else:
                query = query.order_by(BookInfo.title.asc(), BookInfo.created_at.desc(), BookInfo.rating.desc())
        elif by_publication_year:
            query = query.order_by(BookInfo.title.asc(), BookInfo.created_at.desc(), BookInfo.publication_year.desc())
        else:
            query = query.order_by(BookInfo.title.asc(), BookInfo.created_at.desc())
    elif by_rating:
        if by_publication_year:
            query = query.order_by(BookInfo.title.asc(), BookInfo.rating.desc(), BookInfo.publication_year.desc())
        else:
            query = query.order_by(BookInfo.title.asc(), BookInfo.rating.desc())
    elif by_publication_year:
        query = query.order_by(BookInfo.title.asc(), BookInfo.publication_year.desc())
    else:
        query = query.order_by(BookInfo.title.asc())
    
    book_info_list = query.all()

    #---------------------딕셔너리(결과값) 반환---------------------------
    if book_info_list is None:
        return {
            "code": status.HTTP_404_NOT_FOUND,
            "message": "In the request was successfully processed, but there is NoneType object.",
            "result": []
        }
    else:
        if book_info_list:
            return {
                "code": status.HTTP_200_OK,
                "message": "Success to get book information",
                "result": book_info_list
            }
        else:
            return {
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Fail to get book information",
                "result": []
            }


# 개별 도서 정보 조회
@router.get("/book-info/{book_info_id}")
# /{book_info_id}로 요청할 시 422 Unprocessable Entity 오류 발생하여 컨테이너 수정함 - 20230715
def get_book(
    book_info_id: int
    ):
    try:
        book_info = session.query(BookInfo).filter(BookInfo.book_info_id == book_info_id).one()
    except TypeError:
        raise HTTPException(status_code=400, detail="Bad request: book information ID must be integer")
    except: # NotImplementedError 또는 sqlalchemy.exc.NoResultFound - 20230715
        raise HTTPException(status_code=404, detail="Item not found in BookInfo")
    
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
def get_book_holding_list(
        book_info_id: Optional[int] = None,
        donor_name: Optional[str] = None,
        book_status: Optional[int] = None,
        #note: Optional[str] = None,

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
    '''
    if note is not None and not isinstance(note, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid note"
        }
    '''
    #---------------------Query Parameter를 통한 필터링!---------------------------
    query = session.query(Book)
    if book_info_id:
        query = query.filter(Book.book_info_id == book_info_id)
    if donor_name:
        query = query.filter(Book.donor_name.contatins(donor_name))
    if book_status:
        query = query.filter(Book.book_status == book_status)
    #if note:
    #    query = query.filter(Book.note.contains(note))
    
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
    book_holding_list = query.all()
    if book_holding_list is None:
        return {
            "code": status.HTTP_404_NOT_FOUND,
            "message": "In the request was successfully processed, but there is NoneType object.",
            "result": []
        }
    else:
        if book_holding_list:
            return {
                "code": status.HTTP_200_OK,
                "message": "Success to get whole book-holding information list",
                "result": book_holding_list
            }
        else:
            return {
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Fail to get whole book-holding information list",
                "result": []
            }


# 개별 소장 정보 목록 조회
@router.get("/book-holdings/{book_id}")
def get_book_holding(
    book_id: int
    ):
    try:
        book_holding = session.query(Book).filter(Book.book_id == book_id).one()
    except TypeError:
        raise HTTPException(status_code=400, detail="Bad request: book ID must be integer")
    except:
        raise HTTPException(status_code=404, detail="Item not found in Book")
    
    if book_holding:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success to get book-holding information",
            "result": book_holding
        }
    else:
        return {
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Fail to get book-holding information"
        }
    

# 전체 도서 후기 조회
@router.get("/{book_info_id}/reviews")
def get_book_review_list(
    book_info_id: int
    ):
    try:
        book_review_list = session.query(BookReview).filter(BookReview.book_info_id == book_info_id).all()
    except TypeError:
        raise HTTPException(status_code=400, detail="Bad request: book information ID must be integer")
    except:
        raise HTTPException(status_code=404, detail="Item not found in BookReview")
    
    if book_review_list:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success to get book review list",
            "result": book_review_list
        }
    else:
        return {
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Fail to get book review list"
        }


# 개별 도서 후기 조회
@router.get("/{book_info_id}/reviews/{review_id}")
def get_book_review(
    book_info_id: int,
    review_id: int
    ):
    try:
        book_review = session.query(BookReview).filter(BookReview.book_info_id == book_info_id).all()
    except TypeError:
        raise HTTPException(status_code=400, detail="Bad request: book information ID must be integer")
    except:
        raise HTTPException(status_code=404, detail="Item not found in BookReview")
    
    try:
        book_review = book_review.filter(BookReview.review_id == review_id).one()
    except TypeError:
        raise HTTPException(status_code=400, detail="Bad request: review ID must be integer")
    except:
        raise HTTPException(status_code=404, detail="Item not found in BookReview")
    
    if book_review:
        return {
            "code": status.HTTP_200_OK,
            "message": "Success to get book review",
            "result": book_review
        }
    else:
        return {
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Fail to get book review"
        }

'''
# 신착 도서 조회
@router.get("/new-arrival")
def get_new_book_list():
    new_book_list = session.query()
'''