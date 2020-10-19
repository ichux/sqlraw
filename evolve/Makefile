FILE_LOCATION=. /source/results/sqlite_init.sh

help:
	@echo "\`make <target>\` where <target> is one of"
	@echo "  up		bring up the image"
	@echo "  exec		execute commands in the docker environment"
	@echo "  nano		edit files with nano"
	@echo "  vim		edit files with vim"

up:
	@docker-compose up -d

exec:
	@#make exec id=-i; make pm id="-y 1"
	@docker exec -it isql bash -c "$(FILE_LOCATION) && python manage.py $(id)"

nano:
	@#make nano id=results/sqlite/queries/1603119825.sql
	@docker exec -it isql bash -c "nano $(id)"

vim:
	@#make vim id=results/sqlite/queries/1603119825.sql
	@docker exec -it isql bash -c "vim $(id)"
