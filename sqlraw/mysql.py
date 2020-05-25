import functools
import os
import re
import time

import anosql
from mysql.connector.connection import MySQLConnection, errors

from sqlraw import (SCHEMA, DB_URL, MIGRATION_FILE, MIGRATION_FOLDER, migration_files, generate_migration_file, logger)
from sqlraw.mysql_support import (MYSQL_MIGRATION_UP, MYSQL_MIGRATION_DOWN, MYSQL_UP, MYSQL_DOWN, IS_MIGRATION_TABLE,
                                  REVISION_EXISTS)


def mysql(function):
    def wrapper(*args, **kwargs):
        connection = None
        try:

            connection = kwargs['conn'] = MySQLConnection(host=DB_URL.hostname, user=DB_URL.username,
                                                          port=DB_URL.port or 3306, password=DB_URL.password,
                                                          database=DB_URL.path.strip('/'))
            return function(*args, **kwargs)
        except (Exception, errors.Error) as error:
            if connection:
                connection.rollback()
                connection.close()
                logger.error(error)
            raise error

    return functools.update_wrapper(wrapper, function)


class MySQLScheme(object):
    @staticmethod
    def close(conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    @mysql
    def commit(cls, sql, **kwargs):
        conn = kwargs['conn']
        conn.start_transaction()

        cursor = conn.cursor(dictionary=True, buffered=False)
        for _ in cursor.execute(sql, kwargs.get('args'), multi=True):
            pass

        cls.close(conn, cursor)

    @classmethod
    @mysql
    def fetch_one(cls, sql, **kwargs):
        conn = kwargs['conn']

        cursor = conn.cursor(dictionary=True, buffered=False)
        for _ in cursor.execute(sql, kwargs.get('args'), multi=True):
            pass

        result = cursor.fetchone()
        cls.close(conn, cursor)

        return result

    @classmethod
    @mysql
    def fetch_all(cls, sql, **kwargs):
        conn = kwargs['conn']

        cursor = conn.cursor(dictionary=True, buffered=False)
        for _ in cursor.execute(sql, kwargs.get('args'), multi=True):
            pass

        result = cursor.fetchall()
        cls.close(conn, cursor)

        return result


def db_initialise():
    """
    Create the migrations folder and DB table if they are non-existent
    :return: None
    """
    generate_migration_file()
    if not MySQLScheme.fetch_one(IS_MIGRATION_TABLE, **{"args": {'schema': SCHEMA}}):
        with open(MIGRATION_FILE, 'r') as init_sql:
            data = init_sql.read()

            if "CREATE TABLE IF NOT EXISTS migrate_db" not in data:
                when = str(int(time.time()))
                sql_file = os.path.join(MIGRATION_FOLDER, f"{when}.sql")

                with open(sql_file, 'w') as save_sql:
                    up = MYSQL_MIGRATION_UP.format(f"upgrade-{when}", when)
                    down = MYSQL_MIGRATION_DOWN.format(f"downgrade-{when}")

                    save_sql.write("\n\n".join([up, down]))
                    logger.info(f"migration file: {os.path.join('migrations', sql_file)}")
            else:
                when = re.findall('[0-9]+', data)[0]

            generate_migration_file()
            dbi_query = anosql.from_path(MIGRATION_FILE, 'psycopg2')
            MySQLScheme.commit(getattr(dbi_query, f"upgrade_{when}").sql)
            logger.info(f"initial successful migration: {when}")


def db_migrate():
    when = str(int(time.time()))
    sql_file = os.path.join(MIGRATION_FOLDER, f"{when}.sql")

    with open(sql_file, 'w') as save_sql:
        up = MYSQL_UP.format(f"upgrade-{when}", when)
        down = MYSQL_DOWN.format(f"downgrade-{when}", when)

        save_sql.write("\n\n".join([up, down]))
        logger.info(f"migration file: {os.path.join('migrations', sql_file)}")


def db_upgrade():
    generate_migration_file()
    dbu_query = anosql.from_path(MIGRATION_FILE, 'psycopg2')

    for time_step in [_.strip('.sql') for _ in migration_files()]:
        decide = MySQLScheme.fetch_one(REVISION_EXISTS, **{"args": {'revision': time_step}})
        if not decide:
            MySQLScheme.commit(getattr(dbu_query, f"upgrade_{time_step}").sql)
            logger.info(f"successful migration: {time_step}")
        else:
            logger.info(f'migration already exists: {time_step}')


def db_downgrade(step):
    to_use = [_.strip('.sql') for _ in migration_files()]

    # since it's a downgrade, a reverse of the migration is essential
    to_use.reverse()

    generate_migration_file()
    dbd_query = anosql.from_path(MIGRATION_FILE, 'psycopg2')

    try:
        count = 0
        for _ in to_use:
            count += 1
            if MySQLScheme.fetch_one(REVISION_EXISTS, **{"args": {'revision': _}}):
                MySQLScheme.commit(getattr(dbd_query, f"downgrade_{_}").sql)
                logger.info(f"successful downgrade: {_}")
            if count == step:
                break
    except errors.ProgrammingError:
        print("no more downgrade left")


def status():
    to_use = [_.strip('.sql') for _ in migration_files()]
    logger.info(f"migration files: {to_use}")

    for step in to_use:
        try:
            if MySQLScheme.fetch_one(REVISION_EXISTS, **{"args": {'revision': step}}):
                print(f"migrations done: {step}")
        except errors.ProgrammingError:
            print('no present migrations')
