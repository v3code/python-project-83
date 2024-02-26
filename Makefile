lint:
	poetry run pylama ./page_analyzer

install-dev:
	poetry install

install-prod:
	build.sh
	poetry install --only main


build:
	./build.sh


PORT ?= 8000
HOST ?= 127.0.0.1

dev:
	poetry run flask  --app page_analyzer:app --debug run --host ${HOST} --port ${PORT}

install_start_dev:
	poetry install
	make dev


start:
	poetry run gunicorn -w 5 -b ${HOST}:$(PORT) page_analyzer:app