from pydantic import BaseModel, validator
import _datetime
from typing import List


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
            category: int | None = None,
            copied: bool | None = None
    ):
        self.title = title
        self.author = author
        self.major = major
        self.publication_year = publication_year
        self.publisher = publisher
        self.category = category
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


# ADMIN - 도서 정보 등록/수정 RES
class BookInfoOut(BookInfoIn):
    book_info_id: int
    created_at: _datetime.datetime
    updated_at: _datetime.datetime
    rating: float
    valid: bool

# book_id element for holdings list
class HoldingID(BaseModel):
    book_id = int
    __setattr__ = object.__setattr__

    def __init__(self, num):
        self.book_id = num

# ADMIN - 도서 정보 리스트 조회 RES
class BookInfoList(BookInfoOut):
    holdings: List[dict]

# ADMIN - 소장 정보 검색
class BookHoldQuery:
    def __init__(self,
                 donor_name: str | None = None,
                 book_status: int | None = None,
                 book_info_id: int | None = None,
                 get_begin: str | None = None,
                 get_end: str | None = None,
                 ):
        self.book_info_id = book_info_id
        self.donor_name = donor_name
        self.book_status = book_status
        self.get_begin = get_begin
        self.get_end = get_end


# ADMIN - 소장 정보 등록/수정
class BookHoldIn(BaseModel):
    book_info_id: int
    donor_name: str | None = None
    book_status: int
    note: str | None = None

    @validator('book_status')
    def valid_status(cls, book_status: int):
        if book_status < 0 or book_status > 3:
            raise ValueError("book status is out of range!")
        return book_status

    class Config:
        orm_mode = True

# ADMIN - 소장 정보 등록
class BookHoldOut(BookHoldIn):
    created_at: _datetime.datetime
    updated_at: _datetime.datetime
    valid: bool
    book_id: int

# ADMIN - 개별 도서 정보 조회 RES
class BookInfoByID(BookInfoOut):
    books : List[BookHoldOut]

# NOTICE - 전체/개별 공지 조회 RES
class NoticeIn(BaseModel):
    title: str
    notice_content: str
    author_id: int

    class Config:
        orm_mode = True

class NoticeOut(NoticeIn):
    created_at: _datetime.datetime
    updated_at: _datetime.datetime
    valid: bool
    notice_id: int

# OrderBy
class OrderBy:
    def __init__(
        self,
        by_created_at: bool | None = False, # 최신순, 신착도서 조회
        by_rating: bool | None = False, # 평점순, 인기도서 조회
        by_publication_year: bool | None = False # 출판순
        # 여기에 OrderBy 계속 추가하면 됨
    ):
        self.by_created_at = by_created_at
        self.by_rating = by_rating
        self.by_publication_year = by_publication_year