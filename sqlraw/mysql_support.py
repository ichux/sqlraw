MYSQL_UP = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/


INSERT INTO migrate_db (revision) VALUES ('{1}');
"""

MYSQL_DOWN = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/


DELETE FROM migrate_db WHERE revision='{1}';
"""

MYSQL_MIGRATION_UP = """-- name: {0}
/**
  creates the `migrate_db` table 
*/

CREATE TABLE IF NOT EXISTS migrate_db (revision varchar(15) NOT NULL, PRIMARY KEY (revision(15)));
INSERT INTO migrate_db (revision) VALUES ('{1}') ON DUPLICATE KEY UPDATE revision='{1}';
"""

MYSQL_MIGRATION_DOWN = """-- name: {0}
/**
  drops the `migrate_db` table
*/

DROP TABLE IF EXISTS migrate_db;
"""

REVISION_EXISTS = "SELECT revision FROM migrate_db WHERE revision=%(revision)s;"
IS_MIGRATION_TABLE = "SELECT table_rows FROM information_schema.tables WHERE table_schema=%(schema)s " \
                     "AND table_name='migrate_db';"
