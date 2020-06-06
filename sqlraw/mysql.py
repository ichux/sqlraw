import functools
import os
import re
import time

import anosql
from mysql.connector.connection import MySQLConnection, errors

from sqlraw import (SCHEMA, LOGGER, DB_URL, MIGRATION_TABLE, MIGRATION_FILE, MIGRATION_FOLDER, migration_files,
                    generate_migration_file)
from sqlraw.mysql_support import (MYSQL_MIGRATION_UP, MYSQL_MIGRATION_DOWN, MYSQL_UP, MYSQL_DOWN, IS_MIGRATION_TABLE,
                                  REVISION_EXISTS)


def mysql(function):
    """
    Decorates some methods to ensure that the connections are properly closed or rolled back in case of an error.
    :param function: the method if decorates
    :return: method
    """

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
                LOGGER.error(error)
            raise error

    return functools.update_wrapper(wrapper, function)


class MySQLScheme(object):
    @staticmethod
    def close(conn, cursor):
        """
        Commit an open connection, close the cursor and then close the connection
        :param conn: connection
        :param cursor: cursor
        :return: None
        """
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    @mysql
    def commit(cls, sql, **kwargs):
        """
        A high level abstraction that commits queries to the DB
        :param sql: query that will be run against a DB
        :param kwargs: dictionary
        :return: None
        """
        conn = kwargs['conn']

        cursor = conn.cursor(dictionary=True, buffered=False)
        for _ in cursor.execute(sql, kwargs.get('args'), multi=True):
            pass

        cls.close(conn, cursor)

    @classmethod
    @mysql
    def fetch_one(cls, sql, **kwargs):
        """
        Get one result based on the `sql` and `kwargs.get('args')`
        :param sql: query that will be run against a DB
        :param kwargs: dictionary
        :return: a dictionary of result if found, else None
        """
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
        """
        Get more than one result based on the `sql` and `kwargs.get('args')`
        :param sql: query that will be run against a DB
        :param kwargs: a dictionary
        :return: a dictionary of results if found, else None
        """
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

            if f"CREATE TABLE IF NOT EXISTS {SCHEMA}.{MIGRATION_TABLE}" not in data:
                when = str(int(time.time()))
                sql_file = os.path.join(MIGRATION_FOLDER, f"{when}.sql")

                with open(sql_file, 'w') as save_sql:
                    up = MYSQL_MIGRATION_UP.format(f"upgrade-{when}", when, MIGRATION_TABLE, SCHEMA)
                    down = MYSQL_MIGRATION_DOWN.format(f"downgrade-{when}", MIGRATION_TABLE, SCHEMA)

                    save_sql.write("\n\n".join([up, down]))
                    LOGGER.info(f"migration file: {os.path.join('migrations', sql_file)}")
            else:
                when = re.findall('[0-9]+', data)[0]

            generate_migration_file()
            dbi_query = anosql.from_path(MIGRATION_FILE, 'psycopg2')
            MySQLScheme.commit(getattr(dbi_query, f"upgrade_{when}").sql)
            LOGGER.info(f"initial successful migration: {when}")


def db_migrate():
    """
    Generate a new .sql file that you can alter to taste.
    The epoch time of generation is used in naming the generated file
    :return: None
    """
    when = str(int(time.time()))
    sql_file = os.path.join(MIGRATION_FOLDER, f"{when}.sql")

    with open(sql_file, 'w') as save_sql:
        up = MYSQL_UP.format(f"upgrade-{when}", when, MIGRATION_TABLE, SCHEMA)
        down = MYSQL_DOWN.format(f"downgrade-{when}", when, MIGRATION_TABLE, SCHEMA)

        save_sql.write("\n\n".join([up, down]))
        LOGGER.info(f"migration file: {os.path.join('migrations', sql_file)}")


def db_upgrade():
    """
    Runs an upgrade on a DB using the generated `MIGRATION_FILE`
    :return: None
    """
    generate_migration_file()
    dbu_query = anosql.from_path(MIGRATION_FILE, 'psycopg2')

    for time_step in [_.strip('.sql') for _ in migration_files()]:
        decide = MySQLScheme.fetch_one(REVISION_EXISTS, **{"args": {'revision': time_step}})
        if not decide:
            MySQLScheme.commit(getattr(dbu_query, f"upgrade_{time_step}").sql)
            LOGGER.info(f"successful migration: {time_step}")
        else:
            LOGGER.info(f'migration already exists: {time_step}')


def db_downgrade(step):
    """
    Downgrades a DB to a previous version as specified with the `step`
    :param step: number of downgrades to do
    :return: None
    """
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
                LOGGER.info(f"successful downgrade: {_}")
            if count == step:
                break
    except errors.ProgrammingError:
        print("no more downgrade left")


def status():
    """
    Shows the already run migrations
    :return: String
    """
    response = []
    to_use = [_.strip('.sql') for _ in migration_files()]
    LOGGER.info(f"migration files: {to_use}")

    try:
        for step in to_use:
            if MySQLScheme.fetch_one(REVISION_EXISTS, **{"args": {'revision': step}}):
                response.append(f"migrations done  : {step}")
            else:
                response.append(f"migrations undone: {step}")
        return "\n".join(response)
    except errors.ProgrammingError:
        return "No existing migration table"
