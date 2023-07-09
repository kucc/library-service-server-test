from fastapi import APIRouter, Depends, HTTPException
from database import Engineconn
from models import *

engine = Engineconn()
session = engine.sessionmaker()
router = APIRouter(prefix="/books", tags=["books"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

# /books 경로에 대한 핸들러 함수
@router.get("/books")
def get_books():
    books_info = session.query(Book).all()
    if books_info:
        return books_info