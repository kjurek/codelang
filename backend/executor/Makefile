.PHONY: run build clean test lint lint-flake8 lint-bandit

run:
	docker-compose up backend

build:
	docker-compose build

clean:
	docker-compose down --rmi all

test:
	docker-compose run --rm backend_executor_tests

lint: lint-flake8 lint-bandit

lint-flake8:
	docker-compose run --rm --no-deps backend_executor_tests flake8 src
	docker-compose run --rm --no-deps backend_executor_tests flake8 --ignore E501 tests

lint-bandit:
	docker-compose run --rm --no-deps backend_executor_tests bandit -r ./src

requirements.txt: requirements.in
	docker-compose run --rm --no-deps backend_executor_tests pip-compile
	sudo chown $(USER):$(USER) requirements.txt