FROM alpine:latest


RUN apk add --no-cache python3 py3-pip shadow && ln -sf python3 /usr/bin/python

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages
RUN adduser -D -H -s /bin/bash -u 1000 appuser
RUN groupadd -r appgrp
RUN chown -R appuser:appgrp /code

COPY s_app/ .

RUN chown -R appuser:appgrp /code/config

USER appuser

ENV FLASK_APP flask_app.py
ENV FLASK_ENV production
ENV FLASK_RUN_PORT 9091
ENV FLASK_RUN_HOST 0.0.0.0