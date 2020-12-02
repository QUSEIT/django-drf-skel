FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

COPY ./ /home/backend

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev libpq-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && cd /home/backend \
  && cp .env.dev .env \
  && pip install -r requirements.txt

