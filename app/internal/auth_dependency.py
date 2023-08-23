from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from pydantic import BaseModel

app = FastAPI()

# 토큰 생성 및 검증을 위한 키
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 예시용 사용자 데이터베이스
fake_db = {}

# JWT를 검증하기 위한 함수
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# OAuth2PasswordBearer를 사용하여 Authorization 헤더에서 토큰을 추출
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 데이터 모델
class UserProfile(BaseModel):
    username: str
    email: str
    full_name: str

# 엔드포인트 정의
@app.get("/{user_id}/profile")
async def get_user_profile(user_id: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload.get("sub") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]

@app.patch("/{user_id}/profile")
async def update_user_profile(user_id: str, profile_update: UserProfile, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload.get("sub") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = profile_update.dict(exclude_unset=True)
    fake_db[user_id].update(update_data)
    return fake_db[user_id]
