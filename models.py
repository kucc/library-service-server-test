from sqlalchemy import Column, Text, Integer, Boolean, String, TIMESTAMP, Date, DateTime, DECIMAL, SmallInteger
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

Base = declarative_base()

UnsignedInt = INTEGER()
UnsignedInt = UnsignedInt.with_variant(INTEGER(unsigned=True), 'mysql')

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    user_name = Column(String(45), nullable=False, unique=True)
    status = Column(Boolean, nullable=False, default=True)
    email = Column(String(100), nullable=False)
    valid = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class Setting(Base):
    __tablename__ = 'settings'

    setting_id = Column(Integer, primary_key=True)
    service_begin = Column(DateTime, nullable=False)
    service_end = Column(DateTime, nullable=False)
    max_loan_count = Column(Integer, nullable=False)
    loan_period = Column(Integer, nullable=False)
    extend_period = Column(Integer, nullable=False)
    max_request_count = Column(Integer, nullable=False)
    max_request_price = Column(Integer, nullable=False)

class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    admin_status = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    book_info_id = Column(Integer, ForeignKey("book_info.book_info_id"), nullable=False)
    donor_name = Column(String(30))
    book_status = Column(SmallInteger, nullable=False, default=0)
    note = Column(String(255))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    valid = Column(Boolean, nullable=False, default=1)

    bookinfo = relationship("BookInfo", back_poplates="books")

class BookInfo(Base):
    __tablename__ = 'book_info'
    book_info_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    publisher = Column(String(45), nullable=False)
    publication_year = Column(Date, nullable=False)
    image_url = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    version = Column(String(100), nullable=False)
    copied = Column(Boolean, nullable=False, default=0)
    major = Column(Boolean, nullable=False, default=0)
    language = Column(String(10), nullable=False)
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
    author = Column(String(100))
    publication_year = Column(Integer)
    publisher = Column(String(100))
    request_link = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    processing_status = Column(SmallInteger, nullable=False, default=0)
    request_date = Column(DateTime, nullable=False)
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
    extend_status = Column(Boolean, nullable=False, default=0)
    expected_return_date = Column(DateTime, nullable=False)
    return_status = Column(Boolean, nullable=False, default=0)
    return_date = Column(DateTime, nullable=False)
    delay_days = Column(UnsignedInt, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    category_code = Column(String(5), nullable=False)
    category_name = Column(String(30), nullable=False)
    valid = Column(Boolean, nullable=False, default=1)
    
    bookinfo = relationship("BookInfo", back_populates="category")