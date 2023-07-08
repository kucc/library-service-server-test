#  RUN ::
#  uvicorn main:app --reload
from fastapi import FastAPI, Depends, Path, HTTPException, APIRouter
from database import Engineconn
from models import *

app = FastAPI()

engine = Engineconn()
session = engine.sessionmaker()
router = APIRouter()

## root
@app.get("/")
async def root():
    result = {'id': 1}
    return result

# /users 경로에 대한 핸들러 함수
@router.get("/users")
def get_users():
    users_info = session.query(User).all()
    if users_info:
        return users_info

@router.get("/users/{user_id}")
def get_user(user_id: int):
    user_info = session.query(User).filter(User.user_id == user_id).first()
    if user_info: return user_info

# /books 경로에 대한 핸들러 함수
@router.get("/books")
def get_books():
    books_info = session.query(Book).all()
    if books_info:
        return books_info

# /about/notice 경로에 대한 핸들러 함수
@router.get("/about/notice")
def get_notice():
    notice_info = session.query(Notice).all()
    if notice_info:
        return notice_info

# /search 경로에 대한 핸들러 함수
@router.get("/search")
def get_search():
    return {'message' : "search"}

# /admins 경로에 대한 핸들러 함수
@router.get("/admins")
def get_admins():
    admin_info = session.query(Admin).all()
    if admin_info:
        return admin_info


app.include_router(router)