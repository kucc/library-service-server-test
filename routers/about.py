from fastapi import APIRouter, Depends, HTTPException
from database import Engineconn
from models import *

engine = Engineconn()
session = engine.sessionmaker()
router = APIRouter(prefix="/about", tags=["about"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

## about handler
# /about/notice 경로에 대한 핸들러 함수
@router.get("/about/notice")
def get_notice():
    notice_info = session.query(Notice).all()
    if notice_info:
        return notice_info