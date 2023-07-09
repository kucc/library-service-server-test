#  RUN ::
#  uvicorn main:app --reload
from fastapi import FastAPI
from routers import users, books, about
from internal import admins


app = FastAPI()

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

# /search 경로에 대한 핸들러 함수
@app.get("/search")
async def get_search():
    return {'message' : "search"}
