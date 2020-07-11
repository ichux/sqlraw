FROM python:3.8.3-buster

VOLUME /source
WORKDIR /source

# copy directory
COPY sqlraw /source/sqlraw/

# copy files
COPY manage.py mysql_init.sh psql_init.sh sqlite_init.sh requirements.txt /source/

RUN pip install --no-cache-dir -U pip setuptools wheel -r requirements.txt

CMD [ "bash" ]
