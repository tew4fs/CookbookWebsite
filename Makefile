
.DEFAULT_GOAL := build

run:
	pipenv run python manage.py runserver

migrate:
	pipenv run python manage.py migrate

makemigrate:
	pipenv run python manage.py makemigrate

lint:
	pipenv run flake8 .

format:
	pipenv run black .

test:
	pipenv run python manage.py test

docker-build:
	docker build . -t community-cookbooks

build: format lint run