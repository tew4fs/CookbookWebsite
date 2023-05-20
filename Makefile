
.DEFAULT_GOAL := build

run:
	pipenv run python manage.py runserver

migrate:
	pipenv run python manage.py migrate

lint:
	pipenv run flake8 .

format:
	pipenv run black .

test:
	pipenv run python manage.py test

build: format lint run