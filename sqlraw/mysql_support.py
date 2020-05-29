from sqlraw import MIGRATION_TABLE, SCHEMA

MYSQL_UP = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/


INSERT INTO {3}.{2} (revision) VALUES ('{1}');
"""

MYSQL_DOWN = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/


DELETE FROM {3}.{2} WHERE revision='{1}';
"""

MYSQL_MIGRATION_UP = """-- name: {0}
/**
  creates the `{2}` table 
*/

CREATE TABLE IF NOT EXISTS {3}.{2} (revision varchar(15) NOT NULL, PRIMARY KEY (revision(15)));
INSERT INTO {3}.{2} (revision) VALUES ('{1}') ON DUPLICATE KEY UPDATE revision='{1}';
"""

MYSQL_MIGRATION_DOWN = """-- name: {0}
/**
  drops the `{1}` table
*/

DROP TABLE IF EXISTS {2}.{1};
"""

mt = f"{SCHEMA}.{MIGRATION_TABLE}"
REVISION_EXISTS = f"SELECT revision FROM {mt} WHERE revision=%(revision)s;"
IS_MIGRATION_TABLE = f"SELECT table_rows FROM information_schema.tables WHERE table_schema=%(schema)s " \
                     f"AND table_name='{MIGRATION_TABLE}';"
