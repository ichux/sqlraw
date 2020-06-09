FROM python:3.8.3-buster

WORKDIR /source
RUN groupadd -g 999 docker && useradd -r -u 999 -g docker docker

COPY sqlraw /source/
COPY manage.py mysql_init.sh psql_init.sh sqlite_init.sh requirements.txt /source/

RUN pip install -U pip setuptools wheel
RUN pip install -r requirements.txt

USER docker
CMD [ "bash" ]