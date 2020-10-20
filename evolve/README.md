## How to use

You need to copy out this directory named `evolve` and its contents and use it
as a bootstrap for your jobs if you intend to use `docker-compose`. There is a
sample `Makefile`. If your OS supports it, while inside this `evolve` 
directory, type `make`. See the sample output below:

```
`make <target>` where <target> is one of
  up		bring up the image

  exec		execute commands in the docker environment e.g.
  ----		make exec id=-h, make exec id='-y 1'

  nano		edit files with nano e.g.
  ----		make nano id=results/PATH-TO-AN-SQL-FILE.sql

  vim		edit files with vim e.g.
  ----		make vim id=results/PATH-TO-AN-SQL-FILE.sql
```

## volumes
The volumes specified in the docker-compose file works out of the box, while
making some assumptions:

```
    volumes:
      - .:/source/results
```

> Your present directory, identified as the `.` maps to `/source/results`
and as such, all references to files will have `/source/results` or `results`
as part of their beginning.

## make up
Type `make up` to bootstrap a container for you. Once you do this,
`/source/results/sqlite_init.sh` will be used as the configuration. Extra
directory and files will be created in your working directory

## make exec
Examples are `make exec id=-h` or `make exec id='-y 1'`, and you can make up
anyone of your choice, based on what `make exec id=-h` shows you.

`make exec id=-h` == `python manage.py -h`
`make exec id='-y 1'` == `python manage.py -y 1`

And so on.

## make nano AND make vim
Both are the same. But essentially, you can alter the generated files from
inside the container using either `vim` or `nano`. This was created to work 
around file permission issues as experienced on `Ubuntu` If your OS allows you
to alter the generated SQL files without issues, then you might not need to 
use these commands. Sample:

> make vim id=results/PATH-TO-AN-SQL-FILE.sql

In the case above, you need to replace `PATH-TO-AN-SQL-FILE` for the command 
to work appropriately.

## Sample configuration files
>[MySQL](mysql_init.sh) | [PostgreSQL](psql_init.sh) | [SQLite](sqlite_init.sh)

You can edit what is contained in those shown files to taste. But do remember
that `$PWD == /source`

