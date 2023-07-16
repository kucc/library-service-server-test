
from fastapi import APIRouter, status
from database import Engineconn
from models import Admin, Book, BookInfo, BookRequest, User, Notice, Category

engine = Engineconn()
session = engine.sessionmaker()
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
    list = session.query(BookInfo).all()

    for _ in list :

    return {
        "code" : status.HTTP_200_OK,
        "message" : "success to get the list of book information "
        "result" :
    }


@router.get("/{admin_id}/book-info/{book_info_id}")
def get_book_info() :


@router.post('/{admin_id}/book-info')
def enroll_book_info() :


@router.patch('/{admin_id}/book-info/}')
def update_book_info() :


@router.delete('/{admins}/book-info/{book_info_id}')
def delete_book_info():