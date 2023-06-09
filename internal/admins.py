
from fastapi import APIRouter
from database import Engineconn
from models import Admin

engine = Engineconn()
session = engine.sessionmaker()
router = APIRouter(prefix="/admins", tags=["admins"], responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

# /admins 경로에 대한 핸들러 함수
@router.get("/")
def get_admins():
    admin_info = session.query(Admin).all()
    if admin_info:
        return admin_info