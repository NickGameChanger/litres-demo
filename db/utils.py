from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Callable


from aiohttp.web import middleware
import config


async def init_db(app: web.Application) -> None:
    # database_dsn = (
    #     f"postgresql://{config.DB['USER']}:{config.DB['PASSWORD']}"
    #     f"@{config.DB['HOST']}:{config.DB['PORT']}/{config.DB['DATABASE']}"
    # )
    database_dsn = 'postgresql://postgres:postgres@postgres/postgres'
    engine = create_engine(database_dsn, pool_size=25, max_overflow=0)
    app['session_maker'] = sessionmaker(bind=engine)


@middleware
async def sqlalchemy_connection_middleware(
    request: web.Request, handler: Callable
) -> web.Response:
    session = None
    try:
        session = request.app['session_maker']()
        request['session'] = session
        resp = await handler(request)
    finally:
        if session:
            session.close()
    return resp
