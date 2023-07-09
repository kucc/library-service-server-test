# for /users
from fastapi import APIRouter
from database import Engineconn
from models import *

engine = Engineconn()
session = engine.sessionmaker()
router = APIRouter(prefix="/users", tags=["users"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

# /users 경로에 대한 핸들러 함수
@router.get("/")
def get_users():
    users_info = session.query(User).all()
    if users_info:
        return users_info

@router.get("/{user_id}")
def get_user(user_id: int):
    user_info = session.query(User).filter(User.user_id == user_id).first()
    if user_info: return user_info