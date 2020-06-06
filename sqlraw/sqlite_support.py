from sqlraw import MIGRATION_TABLE

SQLITE_UP = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/

INSERT INTO {2} (revision) VALUES ('{1}');
"""

SQLITE_DOWN = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/

DELETE FROM {2} WHERE revision='{1}';
"""

SQLITE_MIGRATION_UP = """-- name: {0}
/**
  creates the `{2}` table 
*/

CREATE TABLE IF NOT EXISTS {2} (revision TEXT NOT NULL PRIMARY KEY);
INSERT INTO {2} (revision) VALUES ('{1}');
"""

SQLITE_MIGRATION_DOWN = """-- name: {0}
/**
  drops the `{1}` table
*/

DROP TABLE IF EXISTS {1};
"""

REVISION_EXISTS = f"SELECT revision FROM {MIGRATION_TABLE} WHERE revision=?;"
IS_MIGRATION_TABLE = f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{MIGRATION_TABLE}';"
