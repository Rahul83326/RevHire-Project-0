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
    username: Optional[str] = None
    role: UserRoleEnum

class User(BaseModel):
    id: int
    username: str
    email: str
    role: UserRoleEnum
    fullname: str
    phonenumber: int
    address: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    fullname: str
    phonenumber: int
    address: str


class ShowJobApplication(BaseModel):
    job_title: str
    user_id: int
    cover_letter: str
    experience: int
    additional_documents: str

class JobApplicationCreate(BaseModel):
    job_title: str
    cover_letter: str
    experience: int
    additional_documents: str

class ShowJobPost(BaseModel):
    com_title: str
    job_description: str
    user_id: int
    salary_range: int
    location: str

class JobPostCreate(BaseModel):
    com_title: str
    job_description: str
    salary_range: int
    location: str
