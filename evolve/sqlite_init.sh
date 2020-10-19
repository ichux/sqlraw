#!/bin/bash

# clear the variables in the terminals, in case you had a change somewhere!
unset SQLRAW_LOGFILE
unset SQLRAW_MIGRATION_FOLDER
unset SQLRAW_MIGRATION_FILE
unset SQLRAW_MIGRATION_TABLE
unset SQLRAW_DB_URL
unset SQLRAW_SCHEMA

export SQLRAW_LOGFILE=$PWD/results/sqlite/attention.log
export SQLRAW_MIGRATION_FOLDER=$PWD/results/sqlite/queries
export SQLRAW_MIGRATION_FILE=$PWD/results/sqlite/migrate.sql
export SQLRAW_MIGRATION_TABLE=migration_data
export SQLRAW_DB_URL=sqlite://$PWD/results/sqlite/sqlraw.db

printenv | grep SQLRAW
