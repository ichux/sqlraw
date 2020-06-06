#!/bin/bash

# to run
#1. cd to the directory that contains this script and run what's in step 2
#2. `source pgsql_init.sh` OR `. pgsql_init.sh`

# clear the variables in the terminals, in case you had a change somewhere!
unset SQLRAW_LOGFILE
unset SQLRAW_MIGRATION_FOLDER
unset SQLRAW_MIGRATION_FILE
unset SQLRAW_MIGRATION_TABLE
unset SQLRAW_DB_URL
unset SQLRAW_SCHEMA

export SQLRAW_LOGFILE=$HOME/Documents/codes/python/project/sqlraw/psql-sqlraw.log
export SQLRAW_MIGRATION_FOLDER=$HOME/Documents/codes/python/project/sqlraw/PSQLQueries
export SQLRAW_MIGRATION_FILE=$HOME/Documents/codes/python/project/sqlraw/psql-migrate.sql
export SQLRAW_MIGRATION_TABLE=migration_data
export SQLRAW_DB_URL=postgres://evolves:b15c6d50b94b2@localhost:6432/evolves
export SQLRAW_SCHEMA=public

printenv | grep SQLRAW
