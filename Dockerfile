FROM python:3.8-slim-buster
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y nano vim && \
    apt-get -y --purge autoremove && apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /source
RUN mkdir -p /source/results

COPY sqlraw /source/sqlraw
COPY manage.py requirements.txt /source/

RUN pip install --no-cache-dir -U pip setuptools wheel -r requirements.txt && \
    rm requirements.txt
VOLUME /source/results
