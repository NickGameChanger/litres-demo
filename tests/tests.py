import unittest

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

import config
from api import api_routes
from db.utils import init_db, sqlalchemy_connection_middleware


# TODO add more tests
class TestGetBookEndpoint(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application(middlewares=[sqlalchemy_connection_middleware])
        app.on_startup.append(init_db)
        for route in api_routes:
            app.add_routes(route)
        return app

    async def test_get_book_success(self):
        # Simulate a GET request to retrieve a book by ID
        book_id = 2  # Replace with a valid book ID
        response = await self.client.get(f'/api/books/{book_id}')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status, 200)

        # Check the response JSON data for the expected results
        result = await response.json()
        self.assertIsInstance(result, dict)  # Ensure the response is a dictionary
        self.assertIn('name', result)  # Check for the presence of a 'name' field

    async def test_get_book_not_found(self):
        # Simulate a GET request to retrieve a non-existent book by ID
        book_id = -123  # Replace with a non-existent book ID
        response = await self.client.get(f'/api/book/{book_id}')

        # Check if the response status code is 404 (Not Found)
        self.assertEqual(response.status, 404)


if __name__ == '__main__':
    unittest.main()
