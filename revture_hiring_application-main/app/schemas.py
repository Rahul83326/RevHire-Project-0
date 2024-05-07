from pydantic import BaseModel
from enum import Enum
from typing import Optional


class UserRoleEnum(str, Enum):
    job_seeker = "job_seeker"
    employer = "employer"

    def __str__(self):
        return str(self.value)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: UserRoleEnum

class User(BaseModel):
    id: int
    username: str
    email: str | None = None
    disabled: bool | None = None
    role: UserRoleEnum

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class showJobApplication(BaseModel):
    job_title: str
    user_id: int


class JobApplicationCreate(BaseModel):
    job_title: str

class ShowJobPost(BaseModel):
    com_title: str
    user_id: int

class JobPostCreate(BaseModel):
    com_title: str