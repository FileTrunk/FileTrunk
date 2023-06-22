FROM python:3.8.7-slim-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt-get update \
&& apt-get -y install g++ libpq-dev gcc unixodbc unixodbc-dev
COPY pyproject.toml poetry.lock /app/
RUN pip install psycopg2-binary
RUN pip install poetry
RUN poetry export -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt
COPY . /app/
RUN apt -y install python3-psycopg2
RUN python3 manage.py collectstatic --no-input
COPY backend-point.sh /
COPY celery-point.sh /
EXPOSE 8000
