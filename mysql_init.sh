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
unset SQLRAW_CHECKS_OFF

export SQLRAW_LOGFILE=$PWD/dbs/mysql/attention.log
export SQLRAW_MIGRATION_FOLDER=$PWD/dbs/mysql/queries
export SQLRAW_MIGRATION_FILE=$PWD/dbs/mysql/migrate.sql
export SQLRAW_MIGRATION_TABLE=migration_data
export SQLRAW_DB_URL=mysql://backend:5ec8b1681@localhost:3306/docker
export SQLRAW_CHECKS_OFF=1

printenv | grep SQLRAW
