from fastapi import APIRouter, status, Depends
from database import get_db
from internal.crudf import *
from internal.schema import NoticeOut, NoticeQuery, PeriodQuery, OrderBy
from models import Notice
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/notices", tags=["notices"])


# /notice 경로에 대한 핸들러 함수
@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=List[NoticeOut],
            response_description="Success to get the list of notice"
            )
async def get_notice_list(
        q: NoticeQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        skip: int | None = 0,
        limit: int | None = 10,
        # get_begin: str = Query(None),
        # get_end: str = Query(None),
        # title: str = Query(None),
        # author: int = Query(None),
        db: Session = Depends(get_db)
):
    return get_list_of_item(model=Notice, skip=skip, limit=limit, user_mode=False, use_update_at=False,
                            q=q, p=p, o=o, db=db)
    # query = db.query(Notice)
    #
    # # Filter by author
    # if author:
    #     query = query.filter(Notice.author_id == author)
    #
    # # Filter by title
    # if title:
    #     query = query.filter(Notice.title.ilike(f"%{title}%"))
    #
    # # Parse begin_date parameter
    # if get_begin is not None:
    #     try:
    #         begin_date = datetime.strptime(get_begin, "%Y-%m-%d")
    #     except ValueError:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                             detail="Invalid begin_date format. It should be in YY-MM-DD format.")
    #     else:
    #         if begin_date > datetime.now():
    #             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                                 detail="Invalid begin_date. It cannot be in the future.")
    # else:
    #     begin_date = datetime.now() - timedelta(days=60)
    #
    # query = query.filter(begin_date <= Notice.updated_at)
    #
    # # Parse end_date parameter
    # if get_end is not None:
    #     try:
    #         end_date = datetime.strptime(get_end, "%Y-%m-%d")
    #     except ValueError:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                             detail="Invalid begin_date format. It should be in YY-MM-DD format.")
    # else:
    #     end_date = datetime.now()
    #
    # query = query.filter(Notice.updated_at <= end_date)
    #
    # notices = query.all()
    # if notices:
    #     return notices
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.get("/{notice_id}",
            status_code=status.HTTP_200_OK,
            response_model=NoticeOut,
            response_description="Success to get the notice by ID"
            )
async def get_notice(
        notice_id: int,
        db: Session = Depends(get_db)
):
    # notice = db.query(Notice).filter(Notice.notice_id == notice_id).first()
    # if notice:
    #     return notice
    # else:
    #     raise ItemKeyValidationError(detail=("notice_id", notice_id))
    return get_item_by_id(model=Notice, index=notice_id, user_mode=True, db=db)