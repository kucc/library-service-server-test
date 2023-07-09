#  RUN ::
#  uvicorn main:app --reload
from fastapi import FastAPI, Depends, Path, HTTPException

app = FastAPI()

## 절대 경로로 변환 필요
from .routers import users, books, about
from .internal import admins

app.include_router(users.router)
app.include_router(books.router)
app.include_router(about.router)
app.include_router(admins.router)

## root
@app.get("/")
async def root():
    result = {'greet': "hello kucc"}
    return result

# @router.post("/auth/login")
# @router.post("user")

# /search 경로에 대한 핸들러 함수
@app.get("/search")
async def get_search():
    return {'message' : "search"}
