FROM python:3.10.13-slim

#SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/yt/src"

RUN apt update

#RUN useradd -rms /bin/bash yt && chmod 777 /opt /run

WORKDIR /yt

RUN mkdir /yt/static && mkdir /yt/media #&& chown -R yt:yt /yt && chmod 755 /yt

COPY ./requirements.txt .

RUN pip install --no-cache-dir --no-warn-script-location --upgrade pip && \
    pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt

COPY . .

#USER yt

#CMD ["gunicorn","-b","0.0.0.0:8001","soaqaz.wsgi:application"]

