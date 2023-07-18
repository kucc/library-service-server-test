
from fastapi import APIRouter, status
from database import EngineConn
from models import Admin, Book, BookInfo, BookRequest, User, Notice, Category

engine = EngineConn()
session = engine.get_session()
router = APIRouter(prefix="/admins", tags=["admins"], responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})


# /admins 경로에 대한 핸들러 함수
@router.get("")
def get_admins():
    return {
        "result" : session.query(Admin).all()
    }

# /admin - 도서 정보(book_info) 관리
@router.get("/book-info")
def get_book_info_list():
    admin_list = session.query(BookInfo).all()
    return {
        "code" : status.HTTP_200_OK,
        "message" : "success to get the list of book information ",
        "result":admin_list
    }
