#  RUN ::
#  uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import admins, auth, books, notice, users

app = FastAPI()


# 라우터 등록
app.include_router(admins.router)
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(notice.router)
app.include_router(users.router)

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "https://library-service-client.vercel.app/"
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