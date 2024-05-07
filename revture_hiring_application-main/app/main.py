from enum import Enum

from typing import Annotated
from . import models
from . import database
from fastapi import Depends, FastAPI, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from .routers import jobapplication, jobposting, users

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(jobposting.router)
app.include_router(jobapplication.router)
app.include_router(users.router)













