from sqlraw import DB_URL, MIGRATION_TABLE, SCHEMA

DSN = f"user={DB_URL.username} password={DB_URL.password} dbname={DB_URL.path.strip('/')} " \
      f"host={DB_URL.hostname} port={DB_URL.port or 5432}"

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

CREATE TABLE IF NOT EXISTS {3}.{2} (revision VARCHAR (15) NOT NULL PRIMARY KEY);
INSERT INTO {3}.{2} (revision) VALUES ('{1}') ON CONFLICT ( revision ) DO NOTHING;"""

PGSQL_MIGRATION_DOWN = """-- name: {0}
/**
  drops the `{1}` table
*/

DROP TABLE IF EXISTS {2}.{1};
"""

mt = f"{SCHEMA}.{MIGRATION_TABLE}"
REVISION_EXISTS = f"SELECT EXISTS (SELECT 1 FROM {mt} WHERE revision=%(revision)s);"
IS_MIGRATION_TABLE = f"SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname=%(schema)s " \
                     f"AND tablename='{MIGRATION_TABLE}');"
