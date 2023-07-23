import datetime
from fastapi import APIRouter, Response, status, HTTPException,Depends
from database import get_db
from internal.key_validation import ItemKeyValidationError, ForeignKeyValidationError
from models import Admin, Book, BookInfo, BookRequest, User, Notice, Category
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel, validator
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix="/admins", tags=["admins"])

#/admins 경로에 대한 핸들러 함수
@router.get("/")
async def get_admins(
        db: Session = Depends(get_db)
):
    admins = db.query(Admin).all()
    return admins

class BookInfoIn(BaseModel):
    title : str
    subtitle : str| None
    category_id : int
    author : str
    publisher : str
    publication_year : int
    image_url : str | None
    version : str | None
    language : str | None
    major : bool | None = False
    copied : bool | None = False

    @validator('language')
    def set_default_language(cls, language: str | None) -> str:
        if language is None:
            return "한국어"
        return language

    class Config:
        orm_mode = True


class BookInfoOut(BookInfoIn):
    book_info_id : int
    created_at : datetime.datetime
    updated_at : datetime.datetime
    rating : float
    valid : bool

    class Config:
        orm_mode = True

#도서 정보(book_info) 리스트 조회
@router.get("/book-info",
            status_code=status.HTTP_200_OK,
            response_description="Success to get whole book-info information list")
async def get_book_info_list(
        skip: int = 0,
        limit: int = 10,
        title: str | None = None,
        author: str | None = None,
        major: bool | None = False,
        publication_year: int | None = None,
        publisher: str | None = None,
        category : int | None = None,

        db: Session = Depends(get_db),

):
    query = db.query(BookInfo)

    if title is not None:
        query = query.filter(BookInfo.title.ilike(f"%{title}%"))
    if author is not None:
        query = query.filter(BookInfo.author.ilike(f"%{author}%"))

    if publisher is not None:
        query = query.filter(BookInfo.publisher.ilike(f"%{publisher}%"))

    if publication_year is not None:
        query = query.filter(BookInfo.publication_year == publication_year)

    if category is not None:
        query = query.filter(BookInfo.category_id == category)

    if major is not None:
        query = query.filter(BookInfo.major == major)

    book_info_list = []
    book_info_data = query.all()

    ## 도서정보 전체 조회시 holdings = {book_id}
    if book_info_data:
        for book_info in book_info_data:
            books = db.query(Book).filter(book_info.book_info_id == Book.book_info_id).all()
            holdings = [{"book_id": book.book_id} for book in books]
            book_info_dict = book_info.__dict__
            book_info_dict['holdings'] = holdings
            book_info_list.append(book_info_dict)
        return book_info_list[skip : skip + limit]
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item not found")


##개별 도서 정보(book_info) 조회
@router.get("/book-info/{book_info_id}")
async def get_book_info(
        book_info_id : int,
        db: Session = Depends(get_db)
):
    query = db.query(BookInfo).options(joinedload(BookInfo.books))
    book_info = query.filter(BookInfo.book_info_id == book_info_id).first()

    if book_info:
        return book_info
    else:
        raise ItemKeyValidationError(detail=("book_info_id", book_info_id))


# 도서 정보 등록
# TODO : validation 문제가 나면 아예 db에 data가 올라가지 않게  \
#  -> 현재 integrity error로 처리, 다른 방법으로 처리 가능한 지 확인 요망
@router.post('/book_info', response_model= BookInfoOut, status_code=status.HTTP_201_CREATED)
async def create_book_info(req:BookInfoIn, db : Session = Depends(get_db)):

    book_info = BookInfo(**req.dict())

    category = db.query(Category).filter_by(category_id = req.category_id).first()
    if category is None:
        raise ForeignKeyValidationError(detail=("category_id", req.category_id))
    try :
        db.add(book_info)

    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig)
        raise HTTPException(status_code=400, detail=error_msg)
    db.commit()
    db.refresh(book_info)
    return book_info

# 도서 정보 수정
@router.patch('/book_info/{book_info_id}',response_model= BookInfoOut, status_code=status.HTTP_200_OK)
async def update_book_info(
        book_info_id : int,
        req : dict,
        db : Session = Depends(get_db)
):
    book_info = db.query(BookInfo).filter_by(book_info_id=book_info_id).first()
    if not book_info :
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