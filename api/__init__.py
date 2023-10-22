from .books import routes as books_routes
from .auth import routes as auth_routes
from .authors import routes as author_routes

api_routes = [books_routes,
              auth_routes,
              author_routes]
