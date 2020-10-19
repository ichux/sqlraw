#!/bin/bash

# clear the variables in the terminals, in case you had a change somewhere!
unset SQLRAW_LOGFILE
unset SQLRAW_MIGRATION_FOLDER
unset SQLRAW_MIGRATION_FILE
unset SQLRAW_MIGRATION_TABLE
unset SQLRAW_DB_URL
unset SQLRAW_SCHEMA
unset SQLRAW_CHECKS_OFF

export SQLRAW_LOGFILE=$PWD/results/mysql/attention.log
export SQLRAW_MIGRATION_FOLDER=$PWD/results/mysql/queries
export SQLRAW_MIGRATION_FILE=$PWD/results/mysql/migrate.sql
export SQLRAW_MIGRATION_TABLE=migration_data
export SQLRAW_DB_URL=mysql://username:password@ipaddress:port/db
export SQLRAW_CHECKS_OFF=1

printenv | grep SQLRAW
