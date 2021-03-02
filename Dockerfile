FROM python:3.9-buster as base
EXPOSE 5000
RUN pip install poetry
RUN mkdir /app
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root --no-dev

COPY . /app/

FROM base as production
ENV FLASK_ENV=production
ENTRYPOINT ["poetry", "run", "gunicorn", "todo_app.app:create_app()", "--bind", "0.0.0.0:5000"]

FROM base as development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

FROM base as test

RUN apt-get update; apt-get install curl -y

#Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    apt-get install ./chrome.deb -y &&\
    rm ./chrome.deb

# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
    echo "Installing chromium webdriver version ${LATEST}" &&\
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
    apt-get install unzip -y &&\
    unzip ./chromedriver_linux64.zip

ENTRYPOINT [ "poetry", "run", "pytest" ]
