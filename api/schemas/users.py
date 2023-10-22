from pydantic import BaseModel, EmailStr
from typing import Optional
from db.models import User


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        str_strip_whitespace = True


class UserSingUp(UserBase):
    secret_code: str
    ...


class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    ...