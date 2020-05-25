import functools
import os
import re
import time

import anosql
import psycopg2
import psycopg2.errors
from psycopg2.extras import NamedTupleCursor

from sqlraw import (SCHEMA, MIGRATION_FILE, MIGRATION_FOLDER, migration_files, generate_migration_file, logger)
from sqlraw.psql_support import (DSN, PGSQL_MIGRATION_UP, PGSQL_MIGRATION_DOWN, PGSQL_UP, PGSQL_DOWN,
                                 IS_MIGRATION_TABLE, REVISION_EXISTS)


def psql(function):
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = kwargs['conn'] = psycopg2.connect(DSN)
            return function(*args, **kwargs)
        except (Exception, psycopg2.DatabaseError, psycopg2.errors.UndefinedTable) as error:
            if connection:
                connection.rollback()
                connection.close()
                logger.error(error)
            raise error

    return functools.update_wrapper(wrapper, function)


class PostgresScheme(object):
    @staticmethod
    def close(conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    @psql
    def commit(cls, sql, **kwargs):
        conn = kwargs['conn']
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        cursor.execute(sql, kwargs.get('args'))
        cls.close(conn, cursor)

    @classmethod
    @psql
    def fetch_one(cls, sql, **kwargs):
        conn = kwargs['conn']
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        cursor.execute(sql, kwargs.get('args'))
        result = cursor.fetchone()
        cls.close(conn, cursor)

        return result

    @classmethod
    @psql
    def fetch_all(cls, sql, **kwargs):
        conn = kwargs['conn']
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        cursor.execute(sql, kwargs.get('args'))
        result = cursor.fetchall()
        cls.close(conn, cursor)

        return result


def db_initialise():
    """
    Create the migrations folder and DB table if they are non-existent
    :return: None
    """
    generate_migration_file()
    if not PostgresScheme.fetch_one(IS_MIGRATION_TABLE, **{"args": {'schema': SCHEMA}}).exists:
        with open(MIGRATION_FILE, 'r') as init_sql:
            data = init_sql.read()

            if "CREATE TABLE IF NOT EXISTS migrate_db" not in data:
                when = str(int(time.time()))
                sql_file = os.path.join(MIGRATION_FOLDER, f"{when}.sql")

                with open(sql_file, 'w') as save_sql:
                    up = PGSQL_MIGRATION_UP.format(f"upgrade-{when}", when)
                    down = PGSQL_MIGRATION_DOWN.format(f"downgrade-{when}")

                    save_sql.write("\n\n".join([up, down]))
                    logger.info(f"migration file: {os.path.join('migrations', sql_file)}")
            else:
                when = re.findall('[0-9]+', data)[0]

            generate_migration_file()
            dbi_query = anosql.from_path(MIGRATION_FILE, 'psycopg2')
            PostgresScheme.commit(getattr(dbi_query, f"upgrade_{when}").sql)
            logger.info(f"initial successful migration: {when}")


def db_migrate():
    when = str(int(time.time()))
    sql_file = os.path.join(MIGRATION_FOLDER, f"{when}.sql")

    with open(sql_file, 'w') as save_sql:
        up = PGSQL_UP.format(f"upgrade-{when}", when)
        down = PGSQL_DOWN.format(f"downgrade-{when}", when)

        save_sql.write("\n\n".join([up, down]))
        logger.info(f"migration file: {os.path.join('migrations', sql_file)}")


def db_upgrade():
    generate_migration_file()
    dbu_query = anosql.from_path(MIGRATION_FILE, 'psycopg2')

    for time_step in [_.strip('.sql') for _ in migration_files()]:
        decide = PostgresScheme.fetch_one(REVISION_EXISTS, **{"args": {'revision': time_step}}).exists
        if not decide:
            PostgresScheme.commit(getattr(dbu_query, f"upgrade_{time_step}").sql)
            logger.info(f"successful migration: {time_step}")
        else:
            logger.info(f'migration already exists: {time_step}')


def db_downgrade(step):
    """
    Downgrade the migration table in steps.

    # shows the migration files
    python manage.py -f

    # downgrade the migration table 2 times
    python manage.py -d 2
    :param step:
    :return: None
    """
    generate_migration_file()

    dbd_query = anosql.from_path(MIGRATION_FILE, 'psycopg2')
    to_use = [_.strip('.sql') for _ in migration_files()]
    to_use.reverse()

    try:
        count = 0
        for _ in to_use:
            count += 1
            if PostgresScheme.fetch_one(REVISION_EXISTS, **{"args": {'revision': _}}).exists:
                PostgresScheme.commit(getattr(dbd_query, f"downgrade_{_}").sql)
                logger.info(f"successful downgrade: {_}")
            if count == step:
                break
    except psycopg2.errors.UndefinedTable:
        print("no more downgrade left")


def status():
    generate_migration_file()
    to_use = [_.strip('.sql') for _ in migration_files()]
    logger.info(f"migration files: {to_use}")

    for step in to_use:
        try:
            if PostgresScheme.fetch_one(REVISION_EXISTS, **{"args": {'revision': step}}).exists:
                print(f"migrations done: {step}")
        except psycopg2.errors.UndefinedTable:
            print("no more downgrade left")
