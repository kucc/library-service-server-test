from fastapi import APIRouter, Query, status
from typing import Optional
from database import Engineconn
from models import Notice, Donor
from datetime import datetime, timedelta

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
    # Validate author and title parameters
    if author is not None and not isinstance(author, int):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid author ID",
        }
    if title is not None and not isinstance(title, str):
        return {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Invalid title",
        }

    query = db.query(Notice)

    # Filter by author
    if author :
        query = query.filter(Notice.author_id == author)

    # Filter by title
    if title :
        query = query.filter(Notice.title.contains(title))

    # Parse begin_date parameter
    if get_begin:
        try:
            begin_date = datetime.strptime(get_begin, "%Y-%m-%d")
        except ValueError:
            return {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid begin_date format. It should be in YYYY-MM-DD format.",
            }
    else:
        begin_date = datetime.today() - timedelta(days=30)
    query = query.filter(Notice.updated_at >= begin_date)

    # Parse end_date parameter
    if get_end:
        try:
            end_date = datetime.strptime(get_end, "%Y-%m-%d")
        except ValueError:
            return {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid end_date format. It should be in YYYY-MM-DD format.",
            }
    else:
        end_date = datetime.today()
    query = query.filter(Notice.updated_at <= end_date)

    notices = query.all()

    if notices:
        return {
            "code": status.HTTP_200_OK,
            "message": "success to get notice",
            "result": notices,
        }
    else :
        return {
            "code" :status.HTTP_204_NO_CONTENT,
            "message" : "In the request was successfully processed, but there is no content to return.",
            "result" : []
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

