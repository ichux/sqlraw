from sqlraw import DB_URL

DSN = f"user={DB_URL.username} password={DB_URL.password} dbname={DB_URL.path.strip('/')} " \
      f"host={DB_URL.hostname} port={DB_URL.port or 5432}"

PGSQL_UP = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/

INSERT INTO migrate_db (revision) VALUES ('{1}');
"""

PGSQL_DOWN = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/

DELETE FROM migrate_db WHERE revision='{1}';
"""

PGSQL_MIGRATION_UP = """-- name: {0}
/**
  creates the `migrate_db` table 
*/

CREATE TABLE IF NOT EXISTS migrate_db (revision VARCHAR (15) NOT NULL PRIMARY KEY);
INSERT INTO migrate_db (revision) VALUES ('{1}') ON CONFLICT ( revision ) DO NOTHING;"""

PGSQL_MIGRATION_DOWN = """-- name: {0}
/**
  drops the `migrate_db` table
*/

DROP TABLE IF EXISTS migrate_db;
"""

REVISION_EXISTS = f"SELECT EXISTS (SELECT 1 FROM migrate_db WHERE revision=%(revision)s);"
IS_MIGRATION_TABLE = "SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname=%(schema)s AND tablename='migrate_db');"
