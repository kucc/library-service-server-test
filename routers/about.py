from fastapi import APIRouter, Query, status
from typing import Optional
from database import Engineconn
from models import Notice, Donor
import datetime

db = Engineconn().sessionmaker()
router = APIRouter(prefix="/about", tags=["about"],responses={201 : {"description" : "Success"}, 400 : {"description" : "Fail"}})

## about handler
# /about/notice 경로에 대한 핸들러 함수
@router.get("/notice")
def get_notices(
    author: Optional[int] = None,
    title: Optional[str] = None,
    get_begin: Optional[str] = None,
    get_end: Optional[str] = None,
) :
    query = db.query(Notice)
    notices = query.all()
    if notices:
        return {
            "code": status.HTTP_200_OK,
            "message": "success to get notice",
            "result": notices,
        }

@router.get("/notice/{notice_id}")
def get_notice(notice_id : int):
    query = db.query(Notice)
    notice = query().filter(Notice.notice_id == notice_id)
    if notice:
        return {
            "code": status.HTTP_200_OK,
            "message": "success to get notice",
            "result": notice
        }

@router.get("/donor")
def get_donors():
    query = db.query(Donor)
    donor_info = query.all()
    if donor_info:
        return donor_info

