#!/bin/bash

# clear the variables in the terminals, in case you had a change somewhere!
unset SQLRAW_LOGFILE
unset SQLRAW_MIGRATION_FOLDER
unset SQLRAW_MIGRATION_FILE
unset SQLRAW_MIGRATION_TABLE
unset SQLRAW_DB_URL
unset SQLRAW_SCHEMA

export SQLRAW_LOGFILE=$PWD/results/psql/attention.log
export SQLRAW_MIGRATION_FOLDER=$PWD/results/psql/queries
export SQLRAW_MIGRATION_FILE=$PWD/results/psql/migrate.sql
export SQLRAW_MIGRATION_TABLE=migration_data
export SQLRAW_DB_URL=postgres://username:password@ipaddress:port/db
export SQLRAW_SCHEMA=public

printenv | grep SQLRAW
