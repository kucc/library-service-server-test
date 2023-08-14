#  RUN ::
#  uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, notice, books
from routers import auth, admins

# 테스트용
from dotenv import load_dotenv

load_dotenv() # take environment variables from .env.

app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)
app.include_router(notice.router)
app.include_router(admins.router)
app.include_router(auth.router)

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # allow cookie  (JWT)
    allow_methods=["*"],
    allow_headers=["*"],
)

# root
@app.get("/")
async def root():
    result = {'greet': "hello kucc"}
    return result

# /search 경로에 대한 핸들러 함수
@app.get("/search")
async def get_search():
    return {'message': "search"}
