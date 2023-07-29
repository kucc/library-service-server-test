from fastapi import APIRouter, Depends, Query, status, HTTPException
from typing import Optional
from database import get_db
from internal.key_validation import ItemKeyValidationError, ForeignKeyValidationError
from internal.schema import *
from models import Book, BookInfo, BookReview, BookRequest
from datetime import datetime, timedelta
from sqlalchemy import asc, desc # asc: 오름차순, desc: 내림차순
from sqlalchemy.orm import Session, joinedload


router = APIRouter(prefix="/books", tags=["books"])


# /books 경로에 대한 핸들러 함수 (전체 도서 정보 조회)
@router.get(
        status_code=status.HTTP_200_OK,
        response_model=List[BookInfoOut],
        response_description="Success to get all book-info information list"
        )
async def get_book_list(
    skip: int | None = 0,
    limit: int | None = 10,
    q: BookInfoQuery = Depends(),

    # 정렬 순서를 정하는 세 가지 Query Parameters, 모두 False일 경우 default는 title의 오름차순으로 정렬된다 - 20230716
    # schema.py로 방식 변경 - 20230728
    o: OrderBy = Depends(),

    get_begin: str | None = None,
    get_end: str | None = None,

    db: Session = Depends(get_db)
    ):
    
    #---------------------Query Parameter를 통한 필터링!---------------------------
    query = db.query(BookInfo)
    if q.author:
        query = query.filter(BookInfo.author.ilike(f"%{q.author}%"))
    if q.publication_year:
        query = query.filter(BookInfo.publication_year == q.publication_year)
    if q.category:
        query = query.filter(BookInfo.category_id == q.category)
    if q.publisher:
        query = query.filter(BookInfo.publisher.ilike(f"%{q.publisher}%"))
    if q.title:
        query = query.filter(BookInfo.title.ilike(f"%{q.title}%"))
    if q.major is True:
        query = query.filter(BookInfo.major is True)
    elif q.major is False:
        query = query.filter(BookInfo.major is False)        

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
    query = query.order_by(BookInfo.title.asc())
    if o.by_the_newest:
        query = query.order_by(BookInfo.created_at.desc())
    if o.by_publication_year:
        query = query.order_by(BookInfo.publication_year.desc())
    if o.by_rating:
        query = query.order_by(BookInfo.rating.desc())
    book_info_list = query.all()

    #---------------------딕셔너리(결과값) 반환---------------------------
    if book_info_list:
        return book_info_list[skip: skip + limit]
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")


# 개별 도서 정보 조회
# /{book_info_id}로 요청할 시 422 Unprocessable Entity 오류 발생하여 컨테이너 수정함 - 20230715
@router.get("/book-info/{book_info_id}",
        status_code=status.HTTP_200_OK,
        response_model=BookInfoByID,
        response_description="Success to get the book-info information"
        )
async def get_book(
    book_info_id: int,
    db: Session = Depends(get_db)
    ):
    query = db.query(BookInfo).options(joinedload(BookInfo.books))
    book_info = query.filter(BookInfo.book_info_id == book_info_id).one()
    
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
        q: BookHoldOut = Depends(),
        o: OrderBy = Depends(),

        get_begin: str | None = None,
        get_end: str | None = None,

        db: Session = Depends(get_db)
    ):

    #---------------------Query Parameter를 통한 필터링!---------------------------
    query = db.query(Book)
    if q.book_info_id:
        query = query.filter(Book.book_info_id == q.book_info_id)
    if q.book_id:
        query = query.filter(Book.book_id == q.book_id)
    if q.donor_name:
        query = query.filter(Book.donor_name.ilike(f"%{q.donor_name}%"))
    if q.book_status:
        query = query.filter(Book.book_status == q.book_status)
    
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
    
    query = query.order_by(Book.book_info_id.asc(), Book.book_id.asc())
    if o.by_the_newest:
        query = query.order_by(Book.updated_at.desc())

    #---------------------딕셔너리(결과값) 반환---------------------------
    book_holding_list = query.all()
    if book_holding_list:
        return book_holding_list[skip: skip + limit]
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")


# 개별 소장 정보 목록 조회
@router.get("/book-holdings/{book_id}",
        status_code=status.HTTP_200_OK,
        response_model=List[BookHoldOut],
        response_description="Success to get the book-holding information"
        )
async def get_book_holding(
    book_id: int,
    db: Session = Depends(get_db)
    ):
    query = db.query(Book)
    book_holding = query.filter(Book.book_id == book_id).one()
    
    if book_holding:
        return book_holding
    else:
        raise ItemKeyValidationError(detail=("book_id", book_id))
    

# 전체 도서 후기 조회
@router.get("/{book_info_id}/reviews",
        status_code=status.HTTP_200_OK,
        response_model=List[BookReviewOut],
        response_description="Success to get all book-review lists"
        )
def get_book_review_list(
    book_info_id: int,
    skip: int | None = 0,
    limit: int | None = 10,

    q: BookReviewOut = Depends(),
    o: OrderBy = Depends(),

    get_begin: str | None = None,
    get_end: str | None = None,

    db: Session = Depends(get_db)
    ):

    #---------------------Query Parameter를 통한 필터링!---------------------------
    query = db.query(BookReview)
    if q.book_info_id:
        query = query.filter(BookReview.book_info_id == q.book_info_id)
    if q.user_id:
        query = query.filter(BookReview.user_id == q.user_id)
    if q.review_id:
        query = query.filter(BookReview.review_id == q.review_id)
    if q.review_content:
        query = query.filter(BookReview.review_content.ilike("f"%{q.review_content}%""))
    
    if get_begin:

    if get_end:
    
    query = query.order_by(BookReview.book_info_id.asc(), BookReview.review_id.asc())
    
    if o.by_created_at:
        return book_review_list



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