import datetime
from fastapi import APIRouter, status, HTTPException, Depends, Request
from database import get_db
from internal.key_validation import ItemKeyValidationError, ForeignKeyValidationError
from internal.schema import *
from internal.crudf import *
from models import Admin, Book, BookInfo, BookRequest, User, Notice, Category
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# TODO - 1. CRUD 용 함수 만들기
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
        db: Session = Depends(get_db),

):
    query = db.query(BookInfo)
    query = filters_by_query(query, BookInfo, q)
    book_info_list = []
    book_info_data = query.all()

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

    book_info = BookInfo(**req.dict())

    category = db.query(Category).filter_by(category_id=req.category_id).first()
    if category is None:
        raise ForeignKeyValidationError(detail=("category_id", req.category_id))
    try:
        db.add(book_info)
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig)
        raise HTTPException(status_code=400, detail=error_msg)
    db.commit()
    db.refresh(book_info)
    return book_info

# 도서 정보 수정
@router.patch('/book-info/{book_info_id}',
              response_model=BookInfoOut,
              status_code=status.HTTP_200_OK,
              response_description="Success to patch the book-info information"
              )
async def update_book_info(
        book_info_id: int,
        req: Request,
        db: Session = Depends(get_db)
):
    book_info = db.query(BookInfo).filter_by(book_info_id=book_info_id).first()
    if not book_info:
        raise ItemKeyValidationError(detail=("book_info_id", book_info_id))

    dict_book_info = book_info.__dict__

    for key in req.keys():
        if key in dict_book_info:
            if isinstance(req[key], type(dict_book_info[key])):
                if key == 'category_id':
                    category_id = req['category_id']
                    fk_category = db.query(Category).filter_by(category_id=category_id).first()
                    if not fk_category:
                        raise ForeignKeyValidationError(detail=("category_id", category_id))
                setattr(book_info, key, req[key])
            else:
                raise HTTPException(status_code=400, detail=f"Invalid value type for column '{key}'.")
        else:
            raise HTTPException(status_code=400, detail=f"Invalid column name: {key}")

    db.commit()
    db.refresh(book_info)

    return book_info

# 도서 정보 삭제
@router.delete('/book-info/{book_info_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Success to remove the book-info information"
               )
async def delete_book_info(
        book_info_id: int,
        db: Session = Depends(get_db)
):
    book_info = db.query(BookInfo).filter_by(book_info_id=book_info_id).first()

    if not book_info:
        raise ItemKeyValidationError(detail=("book_info", book_info_id))

    book_info.valid = 0
    db.commit()
    return None

# 소장 정보 전체 조회
@router.get('/book-holdings/',
            status_code=status.HTTP_200_OK,
            response_model=List[BookHoldOut],
            response_description="Success to get whole book-holdings list"
            )
async def get_book_holdings_info(
        skip: int | None = 0,
        limit: int | None = 10,
        q: BookHoldQuery = Depends(),
        p: PeriodQuery = Depends(),
        db: Session = Depends(get_db)
):
    query = db.query(Book)
    query = filters_by_query(query, Book, q)
    query = filter_by_period(query, Book, p)

    book_holdings_list = query.all()

    if book_holdings_list:
        return book_holdings_list[skip: skip + limit]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

# 소장 정보 개별 조회
@router.get('/book-holdings/{book_id}',
            status_code=status.HTTP_200_OK,
            response_description="Success to get the book-holdings"
            )
async def get_book_holding(
        book_id: int,
        db: Session = Depends(get_db)
):
    book_holding = db.query(Book).filter_by(book_id=book_id).first()
    if book_holding:
        return book_holding
    else:
        raise ItemKeyValidationError(detail=("book_id", book_id))

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
    book = Book(**req.dict())
    book_info = db.query(BookInfo).filter_by(book_info_id=req.book_info_id).first()
    if book_info is None:
        raise ForeignKeyValidationError(detail=("book_info_id", req.book_info_id))
    try:
        db.add(book)

    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig)
        raise HTTPException(status_code=400, detail=error_msg)
    db.commit()
    db.refresh(book)
    return book

# 소장 정보 수정
@router.patch('/book-holdings/{book_id}',
              response_model=BookHoldOut,
              status_code=status.HTTP_200_OK,
              response_description="Success to patch the book-holding"
              )
async def update_book_holding(
        book_id: int,
        req: Request,
        db: Session = Depends(get_db)
):
    book = db.query(Book).filter_by(book_id=book_id).first()
    if not book:
        raise ItemKeyValidationError(detail=("book_id", book_id))

    dict_book = book.__dict__

    for key in req.keys():
        if key in dict_book:
            if isinstance(req[key], type(dict_book[key])):
                if key == 'book_info_id':
                    book_info_id = req['book_info_id']
                    fk_bookinfo = db.query(BookInfo).filter_by(book_info_id=book_info_id).first()
                    if not fk_bookinfo:
                        raise ForeignKeyValidationError(detail=("book_info_id", book_info_id))
                setattr(book, key, req[key])
            else:
                raise HTTPException(status_code=400, detail=f"Invalid value type for column '{key}'.")
        else:
            raise HTTPException(status_code=400, detail=f"Invalid column name: {key}")

    db.commit()
    db.refresh(book)

    return book

# 소장 정보 삭제
@router.delete('/book-info/{book_info_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Success to remove the book holding"
               )
async def delete_book_info(
        book_id: int,
        db: Session = Depends(get_db)
):
    book = db.query(BookInfo).filter_by(book_id=book_id).first()

    if not book:
        raise ItemKeyValidationError(detail=("book_info", book_id))

    book.valid = 0
    db.commit()
    return None



