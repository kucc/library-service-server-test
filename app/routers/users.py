# for /users
from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User

router = APIRouter(prefix="/users", tags=["users"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

# /users 경로에 대한 핸들러 함수
# /users/
@router.get("/")
def get_users(
        db: Session = Depends(get_db)
):
    users_info = db.query(User).all()
    if users_info:
        return users_info

# /users/{user_id}
@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_info = db.query(User).filter(User.user_id == user_id).first()
    if user_info: return user_info