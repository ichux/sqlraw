import argparse

import sqlraw.mysql
import sqlraw.postgresql
from sqlraw import keyword, by_index, display_sql, regex, migration_files, files_by_number
from sqlraw.psql_support import DB_URL


def parse() -> argparse.ArgumentParser:
    """
    Parse the terminal argument(s)
    :return: ArgumentParser
    """
    _ = argparse.ArgumentParser(description='Manage your DB migrations', allow_abbrev=False)

    _.add_argument("-v", "--version", action="version", version="sqlraw version 1.0.3")
    _.add_argument('-p', action='append', dest='collection', default=[], help='print sql to terminal')

    _.add_argument("-k", '--keyword', action='store', type=str, help="checks to see if the supplied word is a keyword")
    _.add_argument("-b", '--by_index', action='store', type=int, help="print sql to terminal by number- start at 1")
    _.add_argument("-n", "--by_number", action="store_true", help="list all the migration files by number")

    _.add_argument("-s", "--status", action="store_true", help="list all migrations registered on the DB")
    _.add_argument("-f", "--files", action="store_true", help="list all the migration files")
    _.add_argument("-r", "--regex", action="store", type=str, help="search migration files with RegEx")

    _.add_argument("-i", "--db_initialise", action="store_true", help="create the migrations table")
    _.add_argument("-m", "--db_migrate", action="store_true", help="create sql file for DB")
    _.add_argument("-u", "--db_upgrade", action="store_true", help="run migration for DB")
    _.add_argument("-d", '--db_downgrade', action='store', type=int, help="downgrade the DB")

    return _


def main():
    """
    The decision box of this application
    :return: None
    """
    parser = parse()
    arguments = parser.parse_args()
    module = sqlraw.postgresql if DB_URL.scheme == 'postgres' else sqlraw.mysql

    if arguments.db_initialise:
        getattr(module, 'db_initialise')()

    if arguments.db_migrate:
        getattr(module, 'db_migrate')()

    if arguments.db_upgrade:
        getattr(module, 'db_upgrade')()

    if arguments.keyword:
        print(keyword(arguments.keyword))

    if arguments.db_downgrade:
        getattr(module, 'db_downgrade')(arguments.db_downgrade)

    if arguments.by_index:
        print(by_index(arguments.by_index))

    if arguments.status:
        print(getattr(module, 'status')())

    if arguments.files:
        print(migration_files())

    if arguments.by_number:
        print(files_by_number())

    if arguments.regex:
        print(regex(arguments.regex))

    if arguments.collection:
        for _ in arguments.collection:
            print(display_sql(_))


if __name__ == '__main__':
    main()
