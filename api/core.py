from aiohttp import web
from db.utils import init_db, sqlalchemy_connection_middleware

from api import api_routes


def init_app(argv: list[str] = None) -> web.Application:
    app = web.Application(middlewares=[sqlalchemy_connection_middleware])
    app.on_startup.append(init_db)
    for route in api_routes:
        app.add_routes(route)

    return app


app = init_app()
