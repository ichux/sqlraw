#!/bin/bash

# to run
#1. cd to the directory that contains this script and run what's in step 2
#2. `source mysql_init.sh` OR `. mysql_init.sh`

# clear the variables in the terminals, in case you had a change somewhere!
unset SQLRAW_LOGFILE
unset SQLRAW_MIGRATION_FOLDER
unset SQLRAW_MIGRATION_FILE
unset SQLRAW_MIGRATION_TABLE
unset SQLRAW_DB_URL
unset SQLRAW_SCHEMA

export SQLRAW_LOGFILE=$HOME/Documents/codes/python/project/sqlraw/mysql-sqlraw.log
export SQLRAW_MIGRATION_FOLDER=$HOME/Documents/codes/python/project/sqlraw/MySQLQueries
export SQLRAW_MIGRATION_FILE=$HOME/Documents/codes/python/project/sqlraw/mysql-migrate.sql
export SQLRAW_MIGRATION_TABLE=migration_data
export SQLRAW_DB_URL=mysql://backend:5ec8b1681@localhost:3306/docker

printenv | grep SQLRAW
