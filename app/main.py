#  RUN ::
#  uvicorn main:app --reload
from fastapi import FastAPI
from routers import users, notice, books
from app.routers import auth, admins

# 테스트용
from dotenv import load_dotenv

load_dotenv() # take environment variables from .env.

app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)
app.include_router(notice.router)
app.include_router(admins.router)
app.include_router(auth.router)

# root
@app.get("/")
async def root():
    result = {'greet': "hello kucc"}
    return result

# /search 경로에 대한 핸들러 함수
@app.get("/search")
async def get_search():
    return {'message': "search"}
