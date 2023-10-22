from pydantic import BaseModel
from typing import Optional
from db.models import Author
from datetime import datetime


class AuthorBase(BaseModel):
    name: str

    class Config:
        str_strip_whitespace = True


class AuthorCreate(AuthorBase):
    ...


class AuthorUpdate(AuthorBase):
    ...


class AuthorOut(AuthorBase):
    created_at: datetime
    updated_at: datetime
