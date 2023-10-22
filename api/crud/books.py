
from sqlalchemy.orm import Session
from db.models import Book, Author
from api.crud import CRUDBase
from api.schemas import BookCreate, BookUpdate
import json
from datetime import datetime
from typing import Optional
from sqlalchemy import or_


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    def create(self, db: Session, *, obj_in: BookCreate) -> Book:
        if obj_in.publish_immediately:
            obj_in.date_published = datetime.utcnow()
        data = obj_in.__dict__
        del data['publish_immediately']
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        return db_obj

    def get_books(
        self, db: Session, author_name: Optional[str] = None, book_name: Optional[str] = None,
        published_at_from: Optional[datetime] = None, published_at_to: Optional[datetime] = None,
        genre: Optional[str] = None, is_fiction: Optional[bool] = None,
        offset: int = 0, limit: int = 100
    ) -> list[Book]:
        filters = [~Book.date_published.is_(None)]
        if author_name:
            filters.append(Author.name.ilike(author_name))
        if book_name:
            filters.append(Book.name.ilike(book_name))
        if genre:
            filters.append(Book.genre.ilike(genre))
        if is_fiction is not None:
            filters.append(Book.is_fiction.is_(is_fiction))
        if published_at_from:
            filters.append(Book.date_published >= published_at_from.date())
        if published_at_to:
            filters.append(Book.date_published <= published_at_to.date())
        books = db.query(
            Book
        ).filter(
            *filters
        ).offset(offset).limit(limit).all()

        return books

    def get_books_by_names(self, db: Session, book_info: list[tuple[str, str]], user_id: int) -> list[Book]:
        filters = [Author.name == author_name and Book.name == book_name for book_name, author_name in book_info]
        return db.query(
            Book
        ).outerjoin(
            Author,
            Author.id == Book.author_id
        ).filter(
            Book.user_id == user_id,
            or_(*filters)
        ).all()

    def get_to_download(self, db: Session, id: int) -> Optional[Book]:
        return db.query(self.model).filter(self.model.id == id).filter(~Book.date_published.is_(None)).first()


book = CRUDBook(Book)
