from pydantic import BaseModel, field_validator
from typing import List
from internal.custom_exception import InvalidDateFormatError
import datetime

# TODO :
#  user_mode : user가 사용하는 api에서는 쿼리 파라미터 제외, admin이 사용하는 api는 쿼리 파라미터로 설정, default true

# get_begin, get_end QUERY class
class PeriodQuery(BaseModel):
    get_begin: str | None = None
    get_end: str | None = None

    @field_validator('get_begin', 'get_end')
    def check_date_format(cls, value):
        if value:
            try:
                value = datetime.datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise InvalidDateFormatError()
            return value

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
        from_attributes = True

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
    valid: bool


# book_id element for holdings list
class HoldingID(BaseModel):
    book_id: int
    __setattr__ = object.__setattr__

    def __init__(self, num):
        self.book_id = num


# BOOKS - 도서 정보 리스트 조회 RES
class BookInfoList(BookInfoOut):
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

    @field_validator('book_status')
    def valid_status(cls, value):
        if value < 0 or value > 3:
            raise ValueError("book status is out of range!")
        return value

    class Config:
        from_attributes = True

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
    valid: bool

# BOOKS - 개별 도서 정보 조회 RES
class BookInfoByID(BookInfoOut):
    books: List[BookHoldOut]

# NOTICE - 전체/개별 공지 등록 REQ
class NoticeIn(BaseModel):
    title: str
    notice_content: str
    author_id: int

    class Config:
        from_attributes = True

class NoticeUpdate(NoticeIn):
    title: str | None
    notice_content: str | None
    author_id: int | None

# NOTICE - 전체/개별 공지 조회, 등록 RES
class NoticeOut(NoticeIn):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    notice_id: int
    valid: bool

# NOTICE - 전체/개별 공지 조회 QUERY
class NoticeQuery:
    def __init__(self,
                 title: str | None = None,
                 author_id: int | None = None,
                 ):
        self.title = title
        self.author_id = author_id

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
        from_attributes = True


# BOOKS - 전체/개별 Review 조회 RES
class BookReviewOut(BookReviewIn):
    review_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    valid: bool


# ADMIN - 카테고리 등록
class CategoryIn(BaseModel):
    category_code: str
    category_name: str

    class Config:
        from_attributes = True

# ADMIN - 카테고리 수정
class CategoryUpdate(CategoryIn):
    category_code: str | None
    category_name: str | None

# ADMIN - 카테고리 RES
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

# ADMIN - 대출 내역 전체 조회 RES
class TakeQueryAdmin:
    def __init__(self,
                 take_loan : bool | None = None,
                 take_return : bool | None = None,
                 take_delay : bool | None = None,
                 take_extend : bool | None = None,
                 target_user : int | None = None,
                 target_book : int | None = None
                 ):
        self.take_loan = take_loan
        self.take_return = take_return
        self.take_delay = take_delay,
        self.take_extend = take_extend,
        self.target_user = target_user,
        self.target_book = target_book

# 임시 대출 등록
class TakeIn(BaseModel):
    user_id: int
    book_id: int
    loan_date: str
    expected_return_date: str

    class Config:
        from_attributes = True

# ADMIN - 대출 이력 수정
class TakeUpdate(TakeIn):
    user_id : int | None
    book_id : int | None
    loan_date : str | None
    extend_status : bool | None
    expected_return_date : str | None
    return_status : bool | None
    return_date : str | None
    delay_days : int | None

# ADMIN - 대출 RES
class TakeOut(TakeIn):
    loan_id : int
    extend_status : bool
    return_status : bool
    return_date : str
    delay_days : int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    valid: bool

# 임시 - 도서 구매 신청 등록 REQ
class BookRequestIn(BaseModel):
    user_id : int
    book_title : str
    request_link : str
    reason : str

    class Config:
        from_attributes = True
       
# 도서 구매 신청 수정 REQ
class BookRequestUpdate(BookRequestIn):
    user_id : int | None
    book_title : str | None
    request_link : str | None
    price: int | None

# 도서 구매 신청 RES
class BookRequestOut(BookRequestIn):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    valid: bool
    price : int

# ADMIN - 도서 신청 REQ
class BookRequestQuery:
    def __init__(self,
                target_user : int | None = None,
                book_title : str | None = None,
                processing_status : int | None = None,
                price : int | None = None,
                ):
        self.target_user = target_user
        self.book_title = book_title
        self.processing_status = processing_status
        self.price = price

# TODO
#  USERS 관련 스키마 만들기
#  Loan* 스키마 검토 (ADMIN의 Take* 스키마와 비교)
# USERS - 전체/개별 회원 정보 조회 QUERY
class UserQuery:
    def __init__(self,
                user_id : int | None = None,
                user_name : str | None = None,
                status : bool | None = None,
                email : str | None = None
            ):
        self.user_id = user_id
        self.user_name = user_name
        self.status = status
        self.email = email

# USERS - 회원 가입 / 회원 정보 수정 REQ
class UserIn(BaseModel):
    user_name: str
    email: str
    password: str

    class Config:
        from_attributes = True

# USERS - 전체/개별 회원 정보 RES
class UserOut(UserIn):
    user_id: int
    status: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    valid: bool

# USERS - 대출 목록 조회 QUERY
class LoanQuery:
    def __init__(self,
                 book_id: int | None = None,
                 user_id: int | None = None,
                 loan_date: str | None = None,
                 extend_status: bool | None = None,
                 expected_return_date: str | None = None,
                 return_status: bool | None = None,
                 return_date: str | None = None,
                 delay_days: int | None = None
            ):
        self.book_id = book_id
        self.user_id = user_id
        self.loan_date = loan_date
        self.extend_status = extend_status
        self.expected_return_date = expected_return_date
        self.return_status = return_status
        self.return_date = return_date
        self.delay_days = delay_days

# USERS - 회원 도서 대출 REQ
class LoanIn(BaseModel):
    book_id : int
    user_id : int
    loan_date : datetime.datetime
    expected_return_date : datetime.datetime

    class Config:
        from_attributes = True

# USERS - 회원 도서 대출 연장 REQ
class LoanExtend(LoanIn):
    extend_status : bool
    expected_return_date : datetime.datetime

    class Config:
        from_attributes = True

# USERS - 회원 도서 대출 반납 REQ
class LoanReturn(LoanExtend):
    return_status : bool
    return_date : datetime.datetime
    delay_days : int

    @field_validator('delay_days')
    def valid_status(cls, value):
        if value < 0:
            raise ValueError("delay days must be nonnegative integer!")
        return value
    
    class Config:
        from_attributes = True

# USERS - 회원 도서 대출, 연장, 반납 RES
class LoanOut(LoanReturn):
    loan_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    valid: bool