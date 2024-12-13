FROM python:3.12.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

COPY ./requirements.txt /app

# COPY pyproject.toml /app

RUN pip install --upgrade pip

# RUN poetry config virtualenvs.create false
# RUN poetry install --no-root --no-interaction --no-ansi

RUN pip install -r requirements.txt  # pip freeze > requirements.txt

COPY . /app/

EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--loop=uvloop", "--port=8000"]
# ENTRYPOINT ["uvicorn", "main:app", "--forwarded-allow-ips='*'", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
