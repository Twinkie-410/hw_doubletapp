FROM python:3.10.13-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/app/src"

RUN apt update

WORKDIR /app

RUN mkdir /app/static && mkdir /app/media

COPY ./requirements.txt .

RUN pip install --no-cache-dir --no-warn-script-location --upgrade pip && \
    pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt

COPY . .

