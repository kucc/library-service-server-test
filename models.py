from sqlalchemy import Column, TEXT, INT, BOOLEAN, String, TIMESTAMP, UniqueConstraint, ColumnDefault, text, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    user_name = Column(String(45), nullable=False, unique=True)
    status = Column(BOOLEAN, nullable=False)
    email = Column(String(100), nullable=False)
    valid = Column(BOOLEAN, nullable=False, default=0)
    status = Column(BOOLEAN, nullable=False, default=1)
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
    admin_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    admin_status = Column(Bool, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Book_review(Base):
    __tablename__ = 'book_review'
    review_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    book_info_id = Column(Integer, nullable=False)
    review_content = Column(String(1000), nullable=False)
    rating = Column(decimal(3,2), nullable=False)
    valid = Column(Bool, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Donor(Base):
    __tablename__ = 'donor'
    donor_id = Column(Integer, primary_key=True)
    donor_name = Column(String(20), nullable=False)

class Book_request(Base):
    __tablename__ = 'book_request'
    book_request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    book_title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    publication_year = Column(Integer, nullable=False)
    publisher = Column(String(100), nullable=False)
    version = Column(String(100), nullable=False)
    major = Column(Bool, nullable=False)
    request_link = Column(String(100), nullable=False)
    reason = Column(String(1000), nullable=False)
    like_count = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    processing_status = Column(Bool, nullable=False)
    request_date = Column(DateTime, nullable=False)
    valid = Column(Bool, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Reservation(Base):
    __tablename__ = 'reservation'
    reservation_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    reservation_status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Book(Base):
    __tablename__ = 'Book'
    book_id = Column(Integer, primary_key=True)
    book_info_id = Column(Integer, nullable=False)
    donor_id = Column(Integer, nullable=False)
    book_status = Column(Integer, nullable=False)
    note = Column(String(1000), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    valid = Column(Bool, nullable=False)

class Book_info(Base):
    __tablename__ = 'book_info'
    book_info_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    subtitle = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    publisher = Column(String(100), nullable=False)
    publication_year = Column(Integer, nullable=False)
    image_url = Column(String(100), nullable=False)
    category_id = Column(Integer, nullable=False)
    copied = Column(String(100), nullable=False)
    version = Column(String(100), nullable=False)
    major = Column(Bool, nullable=False)
    language = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    valid = Column(Bool, nullable=False)

class Ntice(Base):
    __tablename__ = 'notice'
    notice_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    notice_content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    valid = Column(Bool, nullable=False)
    admin_id = Column(Integer, nullable=False)

class Loan(Base):
    __tablename__ = 'loan'
    loan_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    loan_date = Column(DateTime, nullable=False)
    extend_status = Column(Bool, nullable=False)
    expected_return_date = Column(DateTime, nullable=False)
    return_status = Column(Bool, nullable=False)
    return_date = Column(DateTime, nullable=False)
    delay_days = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    category_code = Column(String(100), nullable=False)
    category_name = Column(String(100), nullable=False)
    valid = Column(Bool, nullable=False)