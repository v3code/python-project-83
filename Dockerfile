FROM python:3.10 as base
RUN pip install 'poetry==1.5.1'
RUN apt update
RUN apt install -y make build-essential libpq5
WORKDIR /app
COPY . .
RUN poetry config virtualenvs.create false

FROM base as dev
RUN POETRY_INSTALLER_MAX_WORKERS=1 poetry install --no-interaction

