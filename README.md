# Стек:
python, aiohttp, postgres, sqlachemy

# Описание:
Делаем API сервис, в рамках которого будем давать пользователю доступ к различных литературным произведениям.

# как запустить:
Можно запустить через докер:

Для этого выполнить следующие команды:
  - docker compose build
  - make up
  Накатить миграции: 
  - make yoyo apply

Можно запустить локально, для этого нужно будет поменять конфиги, и порты, согласно тем где у вас будет база данных. 


# ЧТобы запустить тесты, надо выполнить следующую команду:
make my_tests

# Работа с Api

Для того чтобы проверить большинство функционала необходимо создать аккаунт: 
для этого достаточно отправить POST запрос на 
0.0.0.0:8079/api/sing_up c body: {"email": "your_email", "code": 123456} (если код будет не 123456 то регистрация не пройдет успешно.)
В будущем необходимо добавить ручку /otp которая будет отправлять код на почту -> и потом в ручке /api/sing_up будет подтверждение этого кода
P.S. регистрация липовая, в коде берется любой пользователь из базы, просто необходимо создать хотя бы одного, чтобы все ручки правильно функционировали

Для того чтобы создать книги, для начала надо создать авторов, для этого надо стучаться в 
0.0.0.0:8079/api/authors/create c {"author_name": "your_author_name"}
В данной ручке, если удалось создать автора, то API вернет его id, Этот Id будет необходим для того чтобы создать книгу данного автора

# Как создать книгу:
нужно отправить POST запрос в /api/book/create
в body: должны быть следующие поля: id автора, название книги, и сам файл   
    author_id: int, name: str,
Более того следующие поля опциональные: 'Опубликовать_сразу' и жанр
    publish_immediately: bool = False,
    genre: Optional[str] = None,
Их выстовлять надо сразу, если есть желание, потому что изменить их в этой версии невозможно (P.S. разработчики patch не завезли)
publish_immediately - нужно обязательно проставить True, иначе в ручкe /api/books/search данную книги найти не получится

# Как скачать книгу: get запрос в /api/books/{id}/download
если книга отменена, то ее скачать не получится

# Как залить xlsx файл c книгами и авторами:
post - >/api/books/denied
Просто прикрепить данный файл, в результате, вернуться книги которые были найдены в базе, и которым проставили в итоге is_denial
Теперь если попробовать их скачать через /download то ничего не получится

# как просмотреть книги:
get -> /api/books/search
в query параметры для фильтрации можно добавить:
    author_name: str
    book_name: str
    published_at_from: str
    published_at_to: str
    genre: str 
    is_fiction: bool
    offset: int = 0
    limit: int = 100
  
Даты должны быть следующего формата: 'YYYY-MM-DD HH:MM:SS'

# Как просмотреть кокретную книгу:
get -> /api/books/{id:\d+}
Здесь книга появится любая даже если она была заблочена до этого