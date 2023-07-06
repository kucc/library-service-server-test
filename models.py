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
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
