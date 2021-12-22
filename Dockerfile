FROM python:3.9 AS base
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip \
    && pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

FROM base AS api
COPY ./src /app/
CMD ["sh", "run_dev_server.sh"]

FROM base AS service
COPY ./example_service /app/
CMD ["nameko", "run", "service", "--config", "config.yaml"]
