FROM python:3.7.9-buster
EXPOSE 5000
RUN pip install poetry
RUN mkdir /app
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry install

COPY . /app/

ENTRYPOINT poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:5000
