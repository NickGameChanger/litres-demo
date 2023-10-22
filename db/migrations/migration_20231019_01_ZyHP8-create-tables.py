"""
create tables
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE authors (
            id SERIAL NOT NULL,
            name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
            is_blocked BOOLEAN,
            PRIMARY KEY (id)
        );
        """,
        """
            DROP TABLE authors;
        """
    ),
    step(
        """
            CREATE EXTENSION IF NOT EXISTS citext;
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                registration_completed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
                telegram VARCHAR(255),
                is_admin BOOLEAN,
                source VARCHAR(255),
                email citext UNIQUE,

                updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
                created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
            );
        """,
        """
            DROP TABLE users;
        """
    ),
    step(
        """
        CREATE TABLE books (
                id SERIAL NOT NULL,
                name VARCHAR NOT NULL,
                author_id INTEGER NOT NULL,
                is_denied VARCHAR,
                denied_at TIMESTAMP,
                date_published TIMESTAMP,
                updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
                created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
                genre VARCHAR,
                description TEXT,
                user_id INTEGER NOT NULL,
                is_fiction BOOLEAN,
                file_name VARCHAR,
                PRIMARY KEY (id),
                FOREIGN KEY(author_id) REFERENCES authors (id),
                FOREIGN KEY(user_id) REFERENCES users (id)
        )
        """,
        """
            DROP TABLE books;
        """
    ),
]
