from fastapi import APIRouter, Depends
from database import get_db
from models import Book, BookInfo, BookReview, BookRequest
from sqlalchemy.orm import Session

router = APIRouter(prefix="/books", tags=["books"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

# /books 경로에 대한 핸들러 함수
@router.get("/")
def get_books(
        db: Session = Depends(get_db)
):
    books_info = db.query(Book).all()
    if books_info:
        return books_info