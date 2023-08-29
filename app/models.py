from sqlalchemy import Column, Text, Integer, Boolean, String, TIMESTAMP, Date, DateTime, DECIMAL, SmallInteger, text, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from database import Base

UnsignedInt = INTEGER()
UnsignedInt = UnsignedInt.with_variant(INTEGER(unsigned=True), 'mysql')

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    user_name = Column(String(45), nullable=False, unique=True)
    # status(활동 상태): 1(활동), 0(비활동)
    status = Column(Boolean, nullable=False, default=True)
    email = Column(String(100), nullable=False)
    # valid(삭제 여부): 1(유효), 0(삭제)
    valid = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    password = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)

    admin = relationship("Admin", uselist=False, back_populates="user")

class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    # admin_status(관리자 상태): 1(관리자 권한 있음), 0(관리자 권한 없음)
    admin_status = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship("User", back_populates="admin")

class Setting(Base):
    __tablename__ = 'settings'
    setting_id = Column(Integer, primary_key=True)
    service_begin = Column(DateTime, nullable=False)
    service_end = Column(DateTime, nullable=False)
    max_loan_count = Column(UnsignedInt, nullable=False)
    loan_period = Column(UnsignedInt, nullable=False)
    extend_period = Column(UnsignedInt, nullable=False)
    max_request_count = Column(UnsignedInt, nullable=False)
    max_request_price = Column(UnsignedInt, nullable=False)

class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    book_info_id = Column(Integer, ForeignKey("book_info.book_info_id"), nullable=False)
    donor_name = Column(String(30))
    # book_stauts(이용 가능 여부): 0(이용 가능), 1(미등록), 2(분실), 3(폐기)
    book_status = Column(SmallInteger, nullable=False, default=0)
    note = Column(String(255))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    valid = Column(Boolean, nullable=False, default=1)

    bookinfo = relationship("BookInfo", back_populates="books")

class BookInfo(Base):
    __tablename__ = 'book_info'
    book_info_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255))
    author = Column(String(100), nullable=False)
    publisher = Column(String(45), nullable=False)
    publication_year = Column(Date, nullable=False)
    image_url = Column(Text)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    version = Column(String(45))
    copied = Column(Boolean, nullable=False, default=0)
    major = Column(Boolean, default=0)
    rating = Column(DECIMAL(3, 2), default = 0.00)
    language = Column(String(10), default = '한국어')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    valid = Column(Boolean, nullable=False, default=1)

    category = relationship("Category", back_populates="bookinfo")
    books = relationship("Book", back_populates="bookinfo")

class BookReview(Base):
    __tablename__ = 'book_review'
    review_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer,  ForeignKey("user.user_id"), nullable=False)
    book_info_id = Column(Integer, ForeignKey("book_info.book_info_id"), nullable=False)
    review_content = Column(Text, nullable=False)
    rating = Column(DECIMAL(3, 2), nullable=False, default=0.00)
    valid = Column(Boolean, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class BookRequest(Base):
    __tablename__ = 'book_request'
    book_request_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    book_title = Column(String(255), nullable=False)
    request_link = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    # processing_status(처리 상태): 0(구매 대기), 1(구매 완료), 2(구매 반려), 3(신청 취소)
    processing_status = Column(SmallInteger, nullable=False, default=0)
    price = Column(UnsignedInt)
    valid = Column(Boolean, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Notice(Base):
    __tablename__ = 'notice'
    notice_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    author_id = Column(Integer, ForeignKey("admin.admin_id"), nullable=False)
    title = Column(String(255), nullable=False)
    notice_content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    valid = Column(Boolean, nullable=False, default=1)

class Loan(Base):
    __tablename__ = 'loan'
    loan_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    book_id = Column(Integer, ForeignKey("book.book_id"), nullable=False)
    user_id = Column(Integer,  ForeignKey("user.user_id"), nullable=False)
    loan_date = Column(DateTime, nullable=False)
    # extend_status(연장 여부): 1(연장), 0(미연장)
    extend_status = Column(Boolean, nullable=False, default=0)
    expected_return_date = Column(DateTime, nullable=False)
    # return_status(반납 여부): 1(반납), 0(미반납)
    return_status = Column(Boolean, nullable=False, default=0)
    return_date = Column(DateTime)
    delay_days = Column(UnsignedInt, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    category_code = Column(String(5), nullable=False, unique=True)
    category_name = Column(String(30), nullable=False, unique =True)
    valid = Column(Boolean, nullable=False, default=1)
    
    bookinfo = relationship("BookInfo", back_populates="category")