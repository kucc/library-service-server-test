from pydantic import BaseModel, validator
# from typing import List
# from internal.custom_exception import InvalidDateFormatError
# import datetime


# Auth - 로그인 정보

class UserIn(BaseModel):
    email: str

class UserInDB(UserIn):
    password: str

### Auth - 토큰 정보
class Token(BaseModel):
    access_token: str
    token_type: str
    email: str