from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (TEXT, Boolean, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import Session, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from .user import User


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    is_blocked = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    @classmethod
    def find_or_create(cls, db: Session, name: str) -> Author:
        author = db.query(cls).filter(Author.name.ilike(name)).first()
        if not author:
            author = cls(
                name=name
            )
            db.add(author)
            db.commit()
        return author


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship(Author)

    is_denied = Column(String, nullable=True)
    denied_at = Column(DateTime, nullable=True)
    date_published = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    genre = Column(String, nullable=True)
    description = Column(TEXT, nullable=True)
    is_fiction = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade='delete')
    file_name = Column(String, nullable=True)


# TODO
class DeniedRequests(Base):
    __tablename__ = 'denied_requests'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    file_name = Column(String, nullable=True)
# print(CreateTable(Book.__table__).compile(dialect=postgresql.dialect()))
