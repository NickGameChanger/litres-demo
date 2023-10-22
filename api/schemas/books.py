from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from db.models import User


class BookBase(BaseModel):
    name: str
    author_id: int
    genre: Optional[str] = None
    user_id: Optional[int] = None  # if user will be delete we don't want to delete books

    class Config:
        str_strip_whitespace = True


class BookCreate(BookBase):

    publish_immediately: bool = False
    date_published: Optional[datetime] = None
    file_name: str


class BookUpdate(BookBase):
    ...
