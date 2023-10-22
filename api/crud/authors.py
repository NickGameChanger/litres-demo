
from db.models import Author
from api.crud import CRUDBase
from api.schemas import AuthorCreate, AuthorUpdate
from sqlalchemy.orm import Session


class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def search_by_name(
        self, db: Session, *, name: str, offset: int = 0, limit: int = 100
    ) -> list[Author]:
        return db.query(
            Author
        ).filter(
            Author.name.ilike(name)
        ).offset(offset).limit(limit).all()


author = CRUDAuthor(Author)
