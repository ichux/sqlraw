#!/bin/bash

# to run
#1. cd to the directory that contains this script and run what's in step 2
#2. `source sqlite_init.sh` OR `. sqlite_init.sh`

# clear the variables in the terminals, in case you had a change somewhere!
unset SQLRAW_LOGFILE
unset SQLRAW_MIGRATION_FOLDER
unset SQLRAW_MIGRATION_FILE
unset SQLRAW_MIGRATION_TABLE
unset SQLRAW_DB_URL
unset SQLRAW_SCHEMA

export SQLRAW_LOGFILE=$PWD/dbs/sqlite/attention.log
export SQLRAW_MIGRATION_FOLDER=$PWD/dbs/sqlite/queries
export SQLRAW_MIGRATION_FILE=$PWD/dbs/sqlite/migrate.sql
export SQLRAW_MIGRATION_TABLE=migration_data
export SQLRAW_DB_URL=sqlite://$PWD/dbs/sqlite/sqlraw.db

printenv | grep SQLRAW
