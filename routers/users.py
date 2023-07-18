# for /users
from fastapi import APIRouter
from database import EngineConn
from models import User

engine = EngineConn()
session = engine.get_session()
router = APIRouter(prefix="/users", tags=["users"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

# /users 경로에 대한 핸들러 함수
# /users/
@router.get("/")
def get_users():
    users_info = session.query(User).all()
    if users_info:
        return users_info

# /users/{user_id}
@router.get("/{user_id}")
def get_user(user_id: int):
    user_info = session.query(User).filter(User.user_id == user_id).first()
    if user_info: return user_info