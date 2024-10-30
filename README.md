## SQLRAW

This project aims to help you run `DB migrations` using raw sql queries while building applications of any size
and in any programming language. This is achieved by decoupling you from any framework or SQL abstractions
that abound. This is plain and raw SQL, as defined by known SQL standards. `python manage.py -h` will show you
the help manual. However, you need to [set up the project](#how-to-run).

## In doubt?
See your `.log` file for information that are helpful. Some of these information are also posted to the terminal.

## Supported databases and best practises:
For now, SQLite, PostgreSQL (through https://www.psycopg.org/docs/faq.html), MariaDB and 
MySQL (through https://dev.mysql.com/doc/connector-python/en/) are supported and there are plans to 
help it grow into a larger project that will cater to the other databases out there, like mongodb, etc.

For best practises, I have ensured that the PostgreSQL and MySQL links above were followed, and I encourage
you to do the same. As for MariaDB, it has the exact drop-in for MySQL, so, same thing applies, often times.
But then, there might be places that I would have missed and will appreciate if you inform me about such.

`schema` enforcement is on by default. PostgreSQL has a sort of schema that is missing in MySQL/MariaDB 
and you need to be aware of that. `sqlite` in memory type `:memory:` will not work!

## Good to know
1. Either you are using MariaDB or MySQL, you should use the same information like `SQLRAW_DB_URL`
2. Check to see the files, mysql_init.sh or psql_init.sh for choice variables.
3. Even if you did not fill in the variables describe in the `shell scripts` in Step 1 above, some assumptions 
are made where necessary. The project will fail and inform you on what caused it and how to go about solving it.
4. `SQLRAW_CHECKS_OFF=1` will activate the ability to enforce constraints checks during migration(s).

## How to run
1. Use [docker for sqlraw](https://hub.docker.com/r/ichux/sqlraw)
2. Manually install everything by yourself
- Ensure you have **Python v3** installed:
   - I worked with Python 3.8.2.
   - If you like to work using a *virtual environment* then that will also be fine.
- Run `pip install -U pip setuptools wheel` and then activate your Python environment, if need be.
- git clone git@github.com:ichux/sqlraw.git and `cd sqlraw`
- Run `pip install -r requirements.txt`
- Create your own shell script using the sample in [mysql_init.sh](./mysql_init.sh) and [psql_init.sh](./psql_init.sh)
    - Run such by viewing examples of how to run such scripts in the same sample script you used.
    - Do note that `SQLRAW_DB_URL` follows this method `SCHEME://USERNAME:PASSWORD@IPADDRESS:PORT/DATABASE`
    - Do note that the DB details have to match the exact DB you intend to use.
- Test the program: `python manage.py -v` or `python manage.py -h`. See [sample screen shot](./sample.png).

## Script files
Under _How to run_ at the `Step 5` I mentioned you creating your own script from the sample attached to this project.
This utility gives you the ability to have many database migration for different projects, all with their own log files.
So, for instance, assuming you want to or are working with a DB named `school_management`, try to create a script file
named `school_management.sh` that contains the following (if you are using MySQL DB for instance):
```
for var in $(compgen -v | grep '^SQLRAW_'); do
  unset "$var"
done

export SQLRAW_LOGFILE=$HOME/dm/school-management-mysql/smm.log
export SQLRAW_MIGRATION_FOLDER=$HOME/dm/school-management-mysql/queries
export SQLRAW_MIGRATION_FILE=$HOME/dm/school-management-mysql/migrate.sql
export SQLRAW_MIGRATION_TABLE=migration_data
export SQLRAW_DB_URL=mysql://username:password@ipaddress:port/school_management
export SQLRAW_CHECKS_OFF=1
```
Some of the sensible assumptions made is that this program will generate all necessary directories and log files
as long as it has permission to the parent folder. It will also be better if you have a common directory, 
like `$HOME/dm` where all your migrations folders live. In this case, you can properly version them with `git` et al.

The `unset` variables inside the shell script should always be left there at all times. This is just a fail safe
option that clears any variable that is in the terminal. It allowed you to use the same terminal for
several migrations.

## Some assumptions made
1. If you fail to add a `SQLRAW_MIGRATION_FOLDER` a default one will be used. See the [In doubt](#in-doubt) section
2. The default DB port is assumed if you do not add one to your `SQLRAW_DB_URL`
3. The `SQLRAW_MIGRATION_TABLE` is assumed to be `migrate_db` if you did not provide such
3. The `SQLRAW_CHECKS_OFF` is assumed to be `0` if you did not provide such

## Helpers
1. If you cloned this project and want to update it, run `git fetch && git merge origin/master`
2. To avoid SPAM emails, I used a forwarding email in case you need to reach me. It's in [LICENCE.txt](./LICENSE.txt)

## TODO
- [x] Welcome contributors
- [ ] Prepare the project for PyPi (if possible)
- [ ] Speak about this project at conferences
- [ ] Write blog posts
- [ ] Build sample projects on how use it
- [ ] Release Youtube tutorial videos on it
