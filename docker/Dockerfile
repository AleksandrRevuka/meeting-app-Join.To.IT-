FROM python:3.12.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

COPY ./requirements.txt /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt  # pip freeze > requirements.txt

COPY . /app/

EXPOSE 8000

