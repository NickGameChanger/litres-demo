from datetime import datetime
from typing import Any, Optional, Union

from aiohttp.web import (FileResponse, Request, Response, RouteTableDef,
                         StreamResponse, json_response, HTTPNotFound)

from sqlalchemy.orm import Session

import config
from api import crud
from api.decorators import ValidatorType, login_not_required, login_required
from api.schemas import BookCreate
from db.models import Book, User

routes = RouteTableDef()


@routes.get(r'/api/books/{id:\d+}', name='book.get')
@login_not_required()
async def application_file(request: Request, db: Session) -> Response:
    book_id = int(request.match_info['id'])
    book = crud.book.get(db, book_id)
    if not book:
        raise HTTPNotFound(text=f'book with id: {book_id} does not exist')
    return json_response(book.as_dict())


@routes.post('/api/book/create', name='book.create')
@login_required(validator_type=ValidatorType.create_book)
async def create_book(
    request: Request, db: Session, user: User,
    file_name: str,  # TODO find better annotation
    author_id: int, name: str,
    publish_immediately: bool = False,
    genre: Optional[str] = None,
) -> Any:

    author = crud.author.get(db, author_id)
    if not author:
        return json_response(
            {'BadRequest': f'Cannot find author with id: {author_id}'}, status=400)

    create_book = BookCreate(
        name=name,
        author_id=author.id,
        genre=genre,
        user_id=user.id,
        publish_immediately=publish_immediately,
        file_name=file_name,
    )

    created_book: Book = crud.book.create(db, obj_in=create_book)

    return json_response({
        'book_was_created': True,
        'name': created_book.name,
        'created_at': str(created_book.created_at) if created_book.created_at else None,
        'published_at': str(created_book.date_published) if created_book.date_published else None
    })


@routes.get(r'/api/books/{id:\d+}/download')
@login_required(validator_type=ValidatorType.download_book)
async def download_book(
    request: Request, db: Session, user: User, book_id: int
) -> Union[StreamResponse, json_response]:
    book = crud.book.get_to_download(db, book_id)
    if book.is_denied:
        return json_response({'error': 'book is denied'})
    response = FileResponse(path=f'{config.UPLOADS_PATH}/books/{book.file_name}')
    #   Optionally, you can set the content type and headers
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename="{book.file_name}"'
    return response


@routes.get('/api/books/search', name='books.search')
@login_not_required()
async def find_books(request: Request, db: Session) -> Any:
    author_name = request.query.get('author_name')
    book_name = request.query.get('book_name')
    published_at_from = request.query.get('published_at_from')
    published_at_to = request.query.get('published_at_to')
    genre = request.query.get('genre')
    is_fiction = request.query.get('is_fiction')
    offset: int = request.query.get('offset', 0)
    limit: int = request.query.get('limit', 100)
    books = crud.book.get_books(db, author_name, book_name, published_at_from,
                                published_at_to, genre, is_fiction, offset, limit)
    return json_response({'books': [book.as_dict() for book in books]})


@routes.post('/api/books/denied', name='books.denied')
@login_required(validator_type=ValidatorType.denied_books)
async def find_author_by_name(request: Request, db: Session, user: User,
                              books_info: list[tuple[str, str]], file_name: str) -> Response:
    books: list[Book] = crud.book.get_books_by_names(db, books_info, user.id)
    for book in books:
        book.is_denied = True
        book.denied_at = datetime.utcnow()
    db.commit()
    return json_response({'books': [book.as_dict() for book in books]})
