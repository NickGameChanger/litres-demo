PROJECT_NAME=litres

# Common

all: run

run:
	@docker-compose up

stop:
	@docker-compose stop

down:
	@docker-compose down

migrations_apply:
	@docker exec -it litres yoyo apply;

migrations_rollback:
	@docker exec -it litres yoyo rollback;

my_tests:
	@docker exec -it litres python tests/tests.py

psql:
	@docker exec -it postgres psql -U postgres