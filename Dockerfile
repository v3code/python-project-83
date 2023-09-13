FROM python:3.10 as base
RUN pip install 'poetry==1.5.1'
RUN apt update
RUN apt install -y make build-essential libpq5
WORKDIR /app
COPY . .

FROM base as dev
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-interaction

