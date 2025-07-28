FROM python:3.11-slim AS user_microservice

WORKDIR /app

COPY user_microservice/pyproject.toml poetry.lock* /app/

COPY deploy/configs /app/deploy/configs 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY user_microservice/src /app/user_microservice/src

CMD ["uvicorn", "user_microservice.src.main.web:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

