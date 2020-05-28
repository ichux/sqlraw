## SQLRAW

This project intends to help anyone make use of raw sql queries while building applications of any size
and in any programming language. This is achieved by decoupling you from any framework or SQL abstractions
that abound. This is plain and raw SQL, as defined by known SQL standards.

## In doubt?
See your `.log` file for information that are helpful. Some of these information are also posted to the terminal.

## Supported databases and best practises:
For now, PostgreSQL (through https://www.psycopg.org/docs/faq.html), MariaDB and 
MySQL (through https://dev.mysql.com/doc/connector-python/en/) are supported and there are plans to 
help it grow into a larger project that will cater to the other databases out there, like SQLite, etc.

For best practises, I have ensured that the PostgreSQL and MySQL links above were followed, and I encourage
you to do the same. As for MariaDB, it has the exact drop-in for MySQL, so, same thing applies, often times.
But then, there might be places that I would have missed and will appreciate if you inform me about such.

## Good to know
1. Either you DB is MariaDB or MySQL, you should use the same information like `SQLRAW_DB_URL`
2. Check to see the files, mysql_init.sh or psql_init.sh for choice variables.
3. Even if you did not fill in the variables describe in the `shell scripts` in Step 1 above, some assumptions 
are made where necessary. The project will fail and inform you on what caused it and how to go about solving it.

## How to run
1. Ensure you have **Python v3** installed:
   - I worked with Python 3.8.2.
   - If you like to work using a *virtual environment* then that will also be fine.
2. Run `pip install -U pip setuptools wheel` and then activate your Python environment, if need be.
3. git clone git@github.com:ichux/sqlraw.git and `cd sqlraw`
4. Run `pip install -r requirements.txt`
5. Create your own shell script using the sample in [mysql_init.sh](./mysql_init.sh) and [psql_init.sh](./psql_init.sh)
    - Run such by viewing examples of how to run such scripts in the same sample script you used.
    - Do note that `SQLRAW_DB_URL` follows this method `SCHEME://USERNAME:PASSWORD@IPADDRESS:PORT/DATABASE`
    - Do note that the DB details have to match the exact DB you intend to use.
6. Test the program: `python manage.py -v` or `python manage.py -h`. See [sample screen shot](./sample.png).

## Script files
Under _How to run_ at the `Step 5` I mentioned you creating your own script from the sample attached to this project.
This utility gives you the ability to have many database migration for different projects, all with their own log files.
So, for instance, assuming you want to or are working with a DB named `school_management`, try to create a script file
named `school_management.sh` that contains the following (if you are using MySQL DB for instance):
````
unset SQLRAW_LOGFILE
unset SQLRAW_MIGRATION_FOLDER
unset SQLRAW_MIGRATION_FILE
unset SQLRAW_DB_URL
unset SQLRAW_SCHEMA

export SQLRAW_LOGFILE=$HOME/dm/school-management-mysql/smm.log
export SQLRAW_MIGRATION_FOLDER=$HOME/dm/school-management-mysql/queries
export SQLRAW_MIGRATION_FILE=$HOME/dm/school-management-mysql/migrate.sql
export SQLRAW_DB_URL=mysql://username:password@ipaddress:port/school_management
````
Some of the sensible assumptions made is that this program will generate all necessary directories and log files
as long as it has permission to the parent folder. It will also be better if you have a common directory, 
like `$HOME/dm` where all your migrations folders live. In this case, you can properly version them with `git` et al.

The `unset` variables inside the shell script should always be left there at all times. This is just a fail safe
option that clears any variable that is in the terminal. It allowed you to use the same terminal for
several migrations.

## Some assumptions made
1. If you fail to add a `SQLRAW_MIGRATION_FOLDER` a default one will be used. See the [In doubt](#in-doubt) section
2. The default DB port is assumed if you do not add one to your `SQLRAW_DB_URL`

## TODO
- [x] Peer review the code
- [x] Bring the README.md up to date
- [x] Add documentation in the code where necessary
- [ ] Prepare the project for PyPi (if possible)
- [ ] Speak about this project at conferences
- [ ] Write blog posts
- [ ] Build sample projects on how use it
- [ ] Release Youtube tutorial videos on it
- [ ] Welcome contributors