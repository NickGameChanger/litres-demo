import json
import uuid
from datetime import datetime
from typing import Any, Optional

from aiohttp.web import (FileResponse, Request, Response, RouteTableDef,
                         json_response)
from sqlalchemy.orm import Session

import config
from api import crud
from api.decorators import ValidatorType, login_not_required, login_required
from api.schemas import AuthorCreate
from db.models import Author, User

routes = RouteTableDef()


@routes.get('/api/authors/search', name='authors.search')
@login_not_required()
async def find_author_by_name(request: Request, db: Session) -> Response:
    author_name = request.query.get('author_name')
    offset: int = request.query.get('offset', 0)
    limit: int = request.query.get('limit', 100)
    authors = crud.author.search_by_name(db, name=author_name, offset=offset, limit=limit)
    return json_response({'authors': [author.as_dict() for author in authors]})


@routes.post('/api/authors/create', name='authors.create')
@login_required(validator_type=ValidatorType.create_author)
async def create_author(request: Request, db: Session, user: User, author_name: str) -> Response:
    author = crud.author.create(db, obj_in=AuthorCreate(name=author_name))
    return json_response({'author_id': author.id})


@routes.get(r'/api/authors/{id:\d+}', name='authors.get_by_id')
@login_not_required()
async def get_author(request: Request, db: Session) -> Response:
    author_id = request.match_info('id')
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        return json_response({'Value Error': f'have not found authro with id: {author_id}'})
    return json_response({'author': author.as_dict()})
