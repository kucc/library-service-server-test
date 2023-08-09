from pydantic import BaseModel, validator
from typing import List
from app.internal.custom_exception import InvalidDateFormatError
import datetime

# get_begin, get_end QUERY class
class PeriodQuery(BaseModel):
    get_begin: str | None
    get_end: str | None

    @validator('get_begin', 'get_end')
    def check_date_format(cls, value):
        if value:
            try:
                value = datetime.datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise InvalidDateFormatError()
            return value


# TODO ADMIN - BOOK SELECT를 위한 클래스 만들기
# ADMIN - 도서 정보 검색 REQ
class BookInfoQuery:
    def __init__(
            self,
            title: str | None = None,
            author: str | None = None,
            major: bool | None = None,
            publication_year: int | None = None,
            publisher: str | None = None,
            category_id: int | None = None,
            copied: bool | None = None
    ):
        self.title = title
        self.author = author
        self.major = major
        self.publication_year = publication_year
        self.publisher = publisher
        self.category_id = category_id
        self.copied = copied


# ADMIN - 도서 정보 등록 REQ
class BookInfoIn(BaseModel):
    title: str
    subtitle: str | None
    category_id: int
    author: str
    publisher: str
    publication_year: int
    image_url: str | None
    version: str | None
    language: str | None = "한국어"
    major: bool | None = False
    copied: bool | None = False

    class Config:
        orm_mode = True

# ADMIN - 도서 정보 수정 REQ
class BookInfoUpdate(BookInfoIn):
    title: str | None
    category_id: str | None
    author: str | None
    publisher: str | None
    publication_year: str | None

class BookInfoOut(BookInfoIn):
    book_info_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    rating: float


# ADMIN - 도서 정보 등록/수정 RES
class BookInfoOutAdmin(BookInfoOut):
    valid: bool


# book_id element for holdings list
class HoldingID(BaseModel):
    book_id = int
    __setattr__ = object.__setattr__

    def __init__(self, num):
        self.book_id = num


# BOOKS - 도서 정보 리스트 조회 RES
class BookInfoList(BookInfoOut):
    holdings: List[HoldingID]


# ADMIN - 도서 정보 리스트 조회 RES
class BookInfoListAdmin(BookInfoOutAdmin):
    holdings: List[HoldingID]


# ADMIN - 소장 정보 조회 QUERY
class BookHoldQuery:
    def __init__(self,
                 donor_name: str | None = None,
                 book_status: int | None = None,
                 book_info_id: int | None = None
                 ):
        self.book_info_id = book_info_id
        self.donor_name = donor_name
        self.book_status = book_status


# ADMIN - 소장 정보 등록 REQ
class BookHoldIn(BaseModel):
    book_info_id: int
    donor_name: str | None = None
    book_status: int
    note: str | None = None

    @validator('book_status')
    def valid_status(cls, value):
        if value < 0 or value > 3:
            raise ValueError("book status is out of range!")
        return value

    class Config:
        orm_mode = True

# ADMIN - 소장 정보 수정 REQ
class BookHoldUpdate(BookHoldIn):
    book_info_id: int | None
    book_status: int | None
    valid : bool | None

# BOOKS - 소장 정보 조회 RES
class BookHoldOut(BookHoldIn):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    book_id: int

class BookHoldOutAdmin(BookHoldOut):
    valid: bool


# Books - 개별 도서 정보 조회 RES
class BookInfoByID(BookInfoOut):
    books: List[BookHoldOut]


class BookInfoByIDAdmin(BookInfoOutAdmin):
    books: List[BookHoldOutAdmin]


# NOTICE - 전체/개별 공지 등록 REQ
class NoticeIn(BaseModel):
    title: str
    notice_content: str
    author_id: int

    class Config:
        orm_mode = True

class NoticeUpdate(NoticeIn):
    title: str | None
    notice_content: str | None
    author_id: int | None

# NOTICE - 전체/개별 공지 조회, 등록 RES
class NoticeOut(NoticeIn):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    notice_id: int

# NOTICE - 전체/개별 공지 조회 QUERY
class NoticeQuery:
    def __init__(self,
                 title: str | None = None,
                 author_id: int | None = None,
                 ):
        self.title = title
        self.author_id = author_id


# ADMIN - 전체/개별 공지 조회 RES
class NoticeOutAdmin(NoticeOut):
    valid: bool

# Books - 전체 도서 후기 조회 QUERY
class BookReviewQuery:
    def __init__(self,
                user_id : int | None = None,
                rating : int | None = None
            ):
        self.user_id = user_id
        self.rating = rating

class BookReviewAdminQuery:
    def __init__(self,
                user_id : int | None = None,
                book_info_id : int | None = None,
                rating : int | None = None
            ):
        self.user_id = user_id
        self.book_info_id = book_info_id
        self.rating = rating


# USERS - Book Review 등록 REQ
class BookReviewIn(BaseModel):
    user_id: int
    book_info_id: int
    review_content: str
    rating: float

    class Config:
        orm_mode = True


# BOOKS - 전체/개별 Review 조회 RES
class BookReviewOut(BookReviewIn):
    review_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


# ADMIN - 전체/개별 Review 조회 RES
class BookReviewOutAdmin(BookReviewOut):
    valid: bool

# ADMIN - 카테고리 등록
class CategoryIn(BaseModel):
    category_code: str
    category_name: str

    class Config:
        orm_mode = True

# ADMIN - 카테고리 수정
class CategoryUpdate(CategoryIn):
    category_code: str | None
    category_name: str | None

# ADMIN - 카테고리 삭제
class CategoryOut(CategoryIn):
    category_id: int
    valid: bool

# ADMIN - 카테고리 전체 조회
class CategoryQuery:
    def __init__(self,
                category_code : str | None = None,
                category_name : str | None = None,

            ):
        self.category_code = category_code
        self.category_name = category_name

# OrderBy
# 1. None: 정렬 안함
# 2. false: 평점 낮은 순, 등록일/출판년도 오래된 순
# 3. true: 높은 순, 최신순
# 제목은 None인 경우 오름차순 정렬을 기본으로 설정
class OrderBy:
    def __init__(self,
            by_publication_year: bool | None = None, # 출판순: publication_year 기준
            by_rating: bool | None = None, # 평점순: rating 기준
            by_the_newest: bool | None = None, # 최신순: created_at 기준
            by_title: bool | None = False # 제목순: title 기준
        ):
        self.publication_year = by_publication_year
        self.rating = by_rating
        self.created_at = by_the_newest
        self.title = by_title