#  RUN ::
#  uvicorn main:app --reload
from fastapi import FastAPI
from routers import users, books, notice
from internal import admins

# 테스트용
from dotenv import load_dotenv, dotenv_values
load_dotenv() # take environment variables from .env.
import os

app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)
app.include_router(notice.router)
app.include_router(admins.router)

## root
@app.get("/")
async def root():
    result = {'greet': "hello kucc"}
    return result

# /search 경로에 대한 핸들러 함수
@app.get("/search")
async def get_search():
    return {'message' : "search"}
