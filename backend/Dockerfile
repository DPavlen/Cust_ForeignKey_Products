FROM python:3.11.9-slim

ENV SRC_DIR=/app \
    APP_USER=backend-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_PROCESSES=4 \
    GUNICORN_CONNECTIONS=8 \
    GUNICORN_LOGLEVEL='error'

RUN apt-get update && \
    apt-get install -y dos2unix

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app/

RUN poetry lock && poetry install --only main

# Устанавливаем pytest
#RUN poetry add pytest

COPY . /app/

#RUN poetry run pytest --version

CMD ["bash", "/app/run_django.sh"]

RUN poetry install --no-root