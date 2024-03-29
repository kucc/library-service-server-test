from fastapi import APIRouter, Depends, status
from database import get_db
from internal.schemas.schema import *
from internal.crudf import *
from models import *
from sqlalchemy.orm import Session, joinedload

# TODO :
#   CRUD 함수 적용하고 테스트하기
#   DB session 잘 닫히는지 확인하기

# TODO:
#  user_mode, use_updated_at를 쿼리 파라미터 제외
#  use_updated_at : back단에서 설정하고 client가 설정하지 않도록 함
router = APIRouter(prefix="/admins", tags=["admins"])
# /admins 경로에 대한 핸들러 함수
@router.get("")
async def get_admins(
        db: Session = Depends(get_db)
):
    admins = db.query(Admin).all()
    return admins

# 도서 정보(book_info) 리스트 조회
@router.get("/book-info",
            status_code=status.HTTP_200_OK,
            # response_model=List[BookInfoList],
            response_description="Success to get whole book-info information list")
async def get_book_info_list(
        skip: int | None = 0,
        limit: int | None = 10,
        q: BookInfoQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        db: Session = Depends(get_db),

):
    book_info_list = []
    book_info_data = get_list_of_item(model=BookInfo, skip=skip, limit=limit, use_update_at=None,
                                      user_mode=False, q=q, p=p, o=o, init_query=None, db=db)

    # 도서 정보 전체 조회시 holdings = {book_id}
    if book_info_data:
        for book_info in book_info_data:
            books = db.query(Book).filter(book_info.book_info_id == Book.book_info_id).all()
            holdings = [HoldingID(book.book_id) for book in books]
            book_info_dict = book_info.__dict__
            book_info_dict['holdings'] = holdings
            book_info_list.append(book_info_dict)
        return book_info_list[skip: skip + limit]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


# 개별 도서 정보(book_info) 조회
@router.get("/book-info/{book_info_id}",
            response_model=BookInfoByID,
            response_description="Success to get the book-info information"
            )
async def get_book_info(
        book_info_id: int,
        db: Session = Depends(get_db)
):

    query = db.query(BookInfo).options(joinedload(BookInfo.books))
    book_info = query.filter(BookInfo.book_info_id == book_info_id).first()

    if book_info:
        return book_info
    else:
        raise ItemKeyValidationError(detail=("book_info_id", book_info_id))


# 도서 정보 등록
@router.post('/book-info',
             response_model=BookInfoOut,
             status_code=status.HTTP_201_CREATED,
             response_description="Success to create the book-info information"
             )
async def create_book_info(req: BookInfoIn, db: Session = Depends(get_db)):
    return create_item(BookInfo, req, db)

# 도서 정보 수정
@router.patch('/book-info/{book_info_id}',
              response_model=BookInfoOut,
              status_code=status.HTTP_200_OK,
              response_description="Success to patch the book-info information"
              )
async def update_book_info(
        book_info_id: int,
        req: BookInfoUpdate,
        db: Session = Depends(get_db)
):
    return update_item(model=BookInfo, req=req, index=book_info_id, db=db)

# 도서 정보 삭제
@router.delete('/book-info/{book_info_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Success to remove the book-info information"
               )
async def delete_book_info(
        book_info_id: int,
        db: Session = Depends(get_db)
):
    return delete_item(BookInfo, book_info_id, db)

# 소장 정보 전체 조회
@router.get('/book-holdings/',
            status_code=status.HTTP_200_OK,
            response_model=List[BookHoldOut],
            response_description="Success to get whole book-holdings list"
            )
async def get_book_holdings_list(
        skip: int | None = 0,
        limit: int | None = 10,
        use_updated_at: bool | None = False,
        q: BookHoldQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        db: Session = Depends(get_db),
):
    return get_list_of_item(model=Book, skip=skip, limit=limit, use_update_at=use_updated_at, q=q, p=p, o=o, db=db)

# 소장 정보 개별 조회
@router.get('/book-holdings/{book_id}',
            status_code=status.HTTP_200_OK,
            response_description="Success to get the book-holdings"
            )
async def get_book_holding(
        book_id: int,
        db: Session = Depends(get_db),
):
    return get_item_by_id(model=Book, index=book_id, user_mode=False, db=db)

# 소장 정보 등록
@router.post('/book-holdings',
             status_code=status.HTTP_201_CREATED,
             response_model=BookHoldOut,
             response_description="Success to create the book-holding"
             )
async def create_book_holding(
        req: BookHoldIn,
        db: Session = Depends(get_db)
):
    return create_item(Book, req, db)

# 소장 정보 수정
@router.patch('/book-holdings/{book_id}',
              response_model=BookHoldOut,
              status_code=status.HTTP_200_OK,
              response_description="Success to patch the book-holding"
              )
async def update_book_holding(
        book_id: int,
        req: BookHoldUpdate,
        db: Session = Depends(get_db)
):

    return update_item(model=Book, req=req, index=book_id, db=db)


# 소장 정보 삭제
@router.delete('/book-holdings/{book_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Success to remove the book holding"
               )
async def delete_book_holding(
        index: int,
        db: Session = Depends(get_db)
):
    return delete_item(Book, index, db)


# 카테고리 전체 조회
@router.get('/book-category',
            response_model=CategoryOut,
            status_code=status.HTTP_200_OK,
            response_description="Success to get the list of categories"
            )
async def get_category(
        q: CategoryQuery = Depends(),
        db: Session = Depends(get_db),
):
    return get_item_by_column(model=Category, mode=True, columns=q.__dict__, db=db)

# 카테고리 개별 조회
@router.get('/book-category/{category_id}',
            response_model=CategoryOut,
            status_code=status.HTTP_200_OK,
            response_description="Success to get the category"
            )
async def get_category(
        category_id: int,
        db: Session = Depends(get_db)
):
    return get_item_by_id(model=Category, index=category_id, db=db, user_mode=False)


# TODO : 여기서부터 테스트 필요
# 카테고리 등록
@router.post('/book-category',
             response_model=CategoryOut,
             status_code=status.HTTP_201_CREATED,
             response_description="Success to post the category"
             )
async def create_category(
        req: CategoryIn = Depends(),
        db: Session = Depends(get_db)
):
    return create_item(Category, req, db)


# 카테고리 수정
@router.patch('/book-category/{category_id}',
             response_model=CategoryOut,
             status_code=status.HTTP_200_OK,
             response_description="Success to patch the category"
             )
async def update_category(
        category_id: int,
        req: CategoryUpdate = Depends(),
        db: Session = Depends(get_db)
):
    return update_item(model=Category,req=req, index=category_id, db=db)

# 카테고리 삭제
@router.delete('/book-category/{category_id}',
             status_code=status.HTTP_204_NO_CONTENT,
             response_description="Success to patch the category"
             )
async def delete_category(
        category_id: int,
        db: Session = Depends(get_db)
):
    return delete_item(model=Category, index=category_id, db=db)

# 공지 조회
@router.get("/notice",
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
    return get_list_of_item(model=Notice, skip=skip, limit=limit, user_mode=False, use_update_at=False,
                            q=q, p=p, o=o, db=db)

#공지 개별 조회
@router.get("/notice/{notice_id}",
            status_code=status.HTTP_200_OK,
            response_model=NoticeOut,
            response_description="Success to get the notice"
            )
async def get_notice(
        notice_id: int,
        db: Session = Depends(get_db)
):
    return get_item_by_id(model=Notice, index=notice_id, user_mode=False, db=db)

# 공지 등록
@router.post("/notice",
            status_code=status.HTTP_201_CREATED,
            response_model=NoticeOut,
            response_description="Success to post the notice"
             )
async def create_notice(
        req : NoticeIn = Depends(),
        db : Session = Depends(get_db)
):
    return create_item(model=Notice, req=req, db=db)

# 공지 수정
@router.patch("/notice/{notice_id}",
              status_code=status.HTTP_200_OK,
              response_model=NoticeOut,
              response_description="Success to patch the notice"
              )
async def update_notice(
        notice_id : int,
        req : NoticeUpdate = Depends(),
        db: Session = Depends(get_db)
):
    return update_item(model=Notice, req=req, index=notice_id, db=db)

# 공지 삭제
@router.delete("/notice/{notice_id}",
              status_code=status.HTTP_200_OK,
              response_model=NoticeOut,
              response_description="Success to patch the notice"
              )
async def delete_notice(
        notice_id: int,
        db:Session =Depends(get_db)
):
    return delete_item(Notice, notice_id, db)

# 대출 전체 조회  /task
@router.get("/task",
            status_code = status.HTTP_200_OK,
            response_model=List[TakeOut],
            response_description="Success to get the list of loan information"
            )
async def get_task_list(
    q: TakeQueryAdmin = Depends(),
    p: PeriodQuery = Depends(),
    o: OrderBy = Depends(),
    skip: int | None = 0,
    limit: int | None = 10,
    db: Session = Depends(get_db)
):
    return get_list_of_item(model=Loan, skip=skip, limit=limit, q=q, p=p, o=o, user_mode=False, use_update_at=True, db=db)

# 대출, 반납, 연장 내역 개별 조회  /task/{loan_id}
@router.get("/task/{loan_id}",
            status_code = status.HTTP_200_OK,
            response_model=TakeOut,
            response_description="Success to get the loan information"
            )
async def get_task(
        loan_id : int,
        db: Session = Depends(get_db)
):
    return get_item_by_id(model=Loan, index=loan_id, db=db, user_mode=False)

# 대출/반납/연장 정보 수정
@router.patch("/task/{loan_id}",
              status_code= status.HTTP_200_OK,
              response_model=TakeOut,
              response_description="Success to patch the loan information"
              )
async def update_task(
        loan_id: int,
        req : TakeUpdate,
        db: Session = Depends(get_db)
):
    return update_item(model=Loan, req=req, index=loan_id, db=db)

# 대출 정보 삭제
@router.delete("/task/{loan_id}",
              status_code= status.HTTP_204_NO_CONTENT,
              response_description="Success to delete the loan information")
async def delete_task(
        loan_id : int,
        db : Session = Depends(get_db)
):
    return delete_item(model=Loan, index=loan_id, db=db)

# 전체 도서 후기 조회
@router.get("/reviews",
            status_code=status.HTTP_200_OK,
            response_model=List[BookReviewOut],
            response_description="Success to get all book-review lists"
            )
async def get_review_list(
        skip: int | None = 0,
        limit: int | None = 10,
        q: BookReviewQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        db: Session = Depends(get_db)
):
    return get_list_of_item(model=BookReview, skip=skip, limit=limit, user_mode=False, q=q, p=p, o=o, init_query=None,
                            db=db)


# 개별 도서 후기 조회
@router.get("/reviews/{review_id}",
            status_code=status.HTTP_200_OK,
            response_model=BookReviewOut,
            response_description="Success to get the book-review information"
            )
async def get_review(
        review_id: int,
        db: Session = Depends(get_db)
):
    return get_item_by_id(model=BookReview, index=review_id, db=db, user_mode=False)


# 도서 후기 삭제
@router.delete("/reviews/{review_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            response_description="Success to delete the book-review information"
            )
async def get_review(
        review_id: int,
        db: Session = Depends(get_db)
):
    return delete_item(model=BookReview, index=review_id, db=db)

# 전체 도서 신청 내역 조회
@router.get("/book-request",
            status_code=status.HTTP_200_OK,
            response_description="Success to get the list of book-request information"
            )
async def get_book_request_list(
        skip: int | None = 0,
        limit: int | None = 10,
        q: BookRequestQuery = Depends(),
        p: PeriodQuery = Depends(),
        o: OrderBy = Depends(),
        db: Session = Depends(get_db)
):
    return get_list_of_item(model=BookRequest, skip=skip, limit=limit, user_mode=False, q=q, p=p, o=o, init_query=None,
                            db=db)

# 개별 도서 구매 신청 내역 조회
@router.get("/book-request/{book_request_id}",
            status_code=status.HTTP_200_OK,
            response_model=BookRequestOut,
            response_description="Success to get the book-request information"
            )
async def get_book_request(
        request_id: int,
        db: Session = Depends(get_db)
):
    return get_item_by_id(model=BookRequest, index=request_id, db=db, user_mode=False)

# 도서 구매 신청 내역 수정
@router.patch("/book-request/{book_request_id}",
              status_code= status.HTTP_200_OK,
              response_model=TakeOut,
              response_description="Success to patch the book-request information"
              )
async def update_book_request(
        request_id: int,
        req : BookRequestUpdate,
        db: Session = Depends(get_db)
):
    return update_item(model=Loan, req=req, index=request_id, db=db)

# 도서 구매 신청 내역 삭제
@router.delete("/book-request/{book_request_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            response_description="Success to delete the book-review information"
            )
async def get_review(
        request_id: int,
        db: Session = Depends(get_db)
):
    return delete_item(model=BookReview, index=request_id, db=db)
