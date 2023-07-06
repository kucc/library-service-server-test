#  RUN :: 
#  uvicorn main:app --reload
from fastapi import FastAPI, Depends, Path, HTTPException
from pydantic import BaseModel
from database import Engineconn
from models import User


app = FastAPI()

engine = Engineconn()
session = engine.sessionmaker()

@app.get("/")
async def root():
    user = session.query(User).all()
    return user
