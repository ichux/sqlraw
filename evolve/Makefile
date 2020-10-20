FILE_LOCATION=. /source/results/sqlite_init.sh

help:
	@echo "\`make <target>\` where <target> is one of"
	@echo "  up		bring up the image"
	@echo
	@echo "  exec		execute commands in the docker environment e.g."
	@echo "  ----		make exec id=-h, make exec id='-y 1'"
	@echo
	@echo "  nano		edit files with nano e.g."
	@echo "  ----		make nano id=results/PATH-TO-AN-SQL-FILE.sql"
	@echo
	@echo "  vim		edit files with vim e.g."
	@echo "  ----		make vim id=results/PATH-TO-AN-SQL-FILE.sql"
	@echo

up:
	@docker-compose up -d

exec:
	@docker exec -it isql bash -c "$(FILE_LOCATION) && python manage.py $(id)"

nano:
	@#make nano id=results/sqlite/queries/1603119825.sql
	@docker exec -it isql bash -c "nano $(id)"

vim:
	@#make vim id=results/sqlite/queries/1603119825.sql
	@docker exec -it isql bash -c "vim $(id)"
