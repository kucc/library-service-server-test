from fastapi import APIRouter, Depends, status
from app.database import get_db
from app.internal.schemas.schema import NoticeOut, NoticeQuery, PeriodQuery, OrderBy
from app.models import Notice
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
        db: Session = Depends(get_db)
):
    return get_list_of_item(model=Notice, skip=skip, limit=limit, user_mode=True, use_update_at=False,
                            q=q, p=p, o=o, db=db)


@router.get("/{notice_id}",
            status_code=status.HTTP_200_OK,
            response_model=NoticeOut,
            response_description="Success to get the notice"
            )
async def get_notice(
        notice_id: int,
        db: Session = Depends(get_db)
):
    return get_item_by_id(model=Notice, index=notice_id, user_mode=True, db=db)