import logging
import os
import sys
from subprocess import Popen, PIPE
from urllib.parse import urlparse

logger = logging.getLogger('sqlraw')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(os.getenv('SQLRAW_LOGFILE', 'sqlraw.log'))
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

try:
    DB_URL = urlparse(os.getenv('SQLRAW_DB_URL'))
except TypeError:
    logger.error(f"DB_URL is missing. See `mysql_init.sh or pgsql_init.sh` for pointers")
    sys.exit(1)

SCHEMA = os.getenv('SQLRAW_SCHEMA')

if DB_URL.scheme == 'postgres':
    SCHEMA = SCHEMA or 'public'

if DB_URL.scheme == 'mysql':
    SCHEMA = SCHEMA or DB_URL.path.strip('/')

DIRECTORY = os.path.split(os.path.abspath(__file__))[0]
MIGRATION_FOLDER = os.getenv('SQLRAW_MIGRATION_FOLDER', os.path.join(DIRECTORY, 'migrations'))

if not os.path.exists(MIGRATION_FOLDER):
    try:
        os.mkdir(MIGRATION_FOLDER)
    except (Exception,) as error:
        logger.error(error)
        raise error

logger.info(f"MIGRATION_FOLDER: {MIGRATION_FOLDER}")

try:
    MIGRATION_FILE = os.getenv('SQLRAW_MIGRATION_FILE')
except TypeError:
    logger.error(f"MIGRATION_FILE is missing. See `mysql_init.sh or pgsql_init.sh` for pointers")
    sys.exit(1)


def migration_files():
    """
    Gets all the migration files that are found inside the `MIGRATION_FOLDER`
    :return: list
    """
    path, dirs, files = next(os.walk(MIGRATION_FOLDER))
    return sorted([file_ for file_ in files if file_.endswith('.sql')])


def files_by_number():
    """
    Get files by the number at which they are created
    :return: list
    """
    return [(_, num + 1) for num, _ in enumerate(migration_files())]


def generate_migration_file():
    """
    Generates the sql within the `MIGRATION_FILE` that is used by `anosql`
    :return: None
    """
    with open(MIGRATION_FILE, 'w') as sql_queries:
        all_queries = ''
        for each in migration_files():
            with open(os.path.join(MIGRATION_FOLDER, each), 'r') as sql:
                all_queries += f"{sql.read().strip()}\n\n"
        sql_queries.write(all_queries)
        logger.info(f'{MIGRATION_FILE} was generated')


def display_sql(revision):
    """
    Prints sql statements contained in a file by the revision number it appears in the OS
    :param revision: revision number
    :return: String
    """
    if f"{revision}.sql" in migration_files():
        return open(os.path.join(MIGRATION_FOLDER, f"{revision}.sql"), 'r').read()
    return ""


def by_index(step):
    """
    Prints sql statements contained in a file by the number it appears if listed in the OS
    :param step: number of the listed file
    :return: String
    """
    try:
        return open(os.path.join(MIGRATION_FOLDER, migration_files()[step - 1]), 'r').read()
    except IndexError:
        return ""


def regex(pattern):
    """
    Does a pattern search using the system's `find` utility
    :param pattern: a pattern you intend to search for
    :return: String
    """
    cmd = "find " + MIGRATION_FOLDER + " -type f -exec grep -l " + pattern + " {} +"
    out = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = out.communicate()

    if not stderr:
        return stdout.decode()
    else:
        return stderr.decode()
