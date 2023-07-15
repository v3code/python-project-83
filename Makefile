lint:
	poetry run pylama ./page_analyzer

install-dev:
	poetry install

install-prod:
	poetry install --only main

dev:
	poetry run flask --app page_analyzer:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app