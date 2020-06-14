from sqlraw import MIGRATION_TABLE, SCHEMA

TURN_CHECKS_OFF = """/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

"""

MYSQL_UP = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/


INSERT INTO {2} (revision) VALUES ('{1}');
"""

MYSQL_DOWN = """-- name: {0}
/**
  Add your comments here.
  Do remember to adjust the sql statements to taste.
*/


DELETE FROM {2} WHERE revision='{1}';
"""

MYSQL_MIGRATION_UP = """-- name: {0}
/**
  creates the `{2}` table 
*/

CREATE TABLE IF NOT EXISTS {2} (revision varchar(15) NOT NULL, PRIMARY KEY (revision(15)));
INSERT INTO {2} (revision) VALUES ('{1}') ON DUPLICATE KEY UPDATE revision='{1}';
"""

MYSQL_MIGRATION_DOWN = """-- name: {0}
/**
  drops the `{1}` table
*/

DROP TABLE IF EXISTS {1};
"""

REVISION_EXISTS = f"SELECT revision FROM {MIGRATION_TABLE} WHERE revision=%(revision)s;"
IS_MIGRATION_TABLE = f"SELECT table_rows FROM information_schema.tables WHERE table_schema=%(schema)s " \
                     f"AND table_name='{MIGRATION_TABLE}';"
