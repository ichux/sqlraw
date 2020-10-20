from sqlraw import DB_URL, MIGRATION_TABLE, SCHEMA

DSN = f"user={DB_URL.username} password={DB_URL.password} " \
      f"dbname={DB_URL.path.strip('/')} host={DB_URL.hostname} " \
      f"port={DB_URL.port or 5432}"

PGSQL_UP = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/

INSERT INTO {3}.{2} (revision) VALUES ('{1}');
"""

PGSQL_DOWN = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/

DELETE FROM {3}.{2} WHERE revision='{1}';
"""

PGSQL_MIGRATION_UP = """-- name: {0}
/**
  creates the `{2}` table 
*/

"""
SUBST1 = f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};" if SCHEMA != 'public' else ''
SUBST2 = """
CREATE TABLE IF NOT EXISTS {3}.{2} (revision VARCHAR (15) NOT NULL PRIMARY KEY);
INSERT INTO {3}.{2} (revision) VALUES ('{1}') ON CONFLICT ( revision ) DO NOTHING;
"""

PGSQL_MIGRATION_UP = PGSQL_MIGRATION_UP + SUBST1 + SUBST2

PGSQL_MIGRATION_DOWN = """-- name: {0}
/**
  drops the `{1}` table
*/

DROP TABLE IF EXISTS {2}.{1};
"""
SUBSTITUTE = f"DROP SCHEMA IF EXISTS {SCHEMA};" if SCHEMA != 'public' else ''
PGSQL_MIGRATION_DOWN = PGSQL_MIGRATION_DOWN + SUBSTITUTE

mt = f"{SCHEMA}.{MIGRATION_TABLE}"
REVISION_EXISTS = f"SELECT EXISTS (SELECT 1 FROM {mt} WHERE revision=%(revision)s);"
IS_MIGRATION_TABLE = f"SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname=%(schema)s " \
                     f"AND tablename='{MIGRATION_TABLE}');"
