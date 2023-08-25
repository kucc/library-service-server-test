from pydantic import BaseModel, validator
from typing import Union

# 일반 사용자와 관리자 공통의 필드가 정의된 스키마
class AuthBaseUser(BaseModel):
    user_id: int
    email: str | None = None
    user_name: str | None = None
    status: bool | None = None
    valid: bool | None = None
    # access_token: str

# 일반 사용자 스키마
class AuthUser(AuthBaseUser):
    pass

# 관리자 스키마
class AuthAdmin(AuthBaseUser):
    admin_id: int
    admin_status: bool

# 일반 사용자와 관리자 스키마를 합친 스키마
class AuthUserResponse(BaseModel):
    user: Union[AuthUser, AuthAdmin]