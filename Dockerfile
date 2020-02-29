FROM python:3.8.1-slim-buster

# Setup paths and users
ENV APP_HOME="/home/app"
RUN useradd -m -d ${APP_HOME} app
WORKDIR ${APP_HOME}

# Install system dependencies
RUN pip -qq --no-cache-dir install 'poetry==1.0.4'

# Install project & dependencies (check .dockerignore for exceptions)
COPY . .
RUN apt-get update\
    && apt-get install -y build-essential git \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-dev

# Set permissions and user
RUN chown -R app:app .
USER app

# Run
CMD []
