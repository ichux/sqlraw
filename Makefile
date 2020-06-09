help:
	@echo "\`make <target>\` where <target> is one of"
	@echo "  build			build the image"
	@echo "  bash			to make bash for the docker environment"
	@echo "  access		to make the environment fit by changing the modes"

clean:
	@find . -name '__MACOSX' -type d -print0 | xargs -0 /bin/rm -rf '{}'
	@find . -name '__pycache__' -type d -print0 | xargs -0 /bin/rm -rf '{}'
	@find . -iname 'Thumbs.db' -delete
	@find . -iname '*.url' -delete
	@find . -iname '*.pyc' -delete
	@find . -iname '.DS_Store' -delete
	@find . -iname 'DS_Store' -delete

build: clean
	@docker-compose --project-name query build

bash:
	@docker-compose --project-name query run --rm --name sql-raw sqlraw

access:
	@docker exec -u root sql-raw chmod 777 .

upload:
	@docker login
	@docker tag query_sqlraw:latest ichux/sqlraw:latest
	@docker push ichux/sqlraw:latest