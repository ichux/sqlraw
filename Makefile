help:
	@echo "\`make <target>\` where <target> is one of"
	@echo "  build			build the image"
	@echo "  bash			to make bash for the docker environment"
	@echo "  access		to make the environment fit by changing the modes"
	@echo "  tag			tags the image"
	@echo "  upload		uploads to docker hub"

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
	@make tag

bash:
	@#CURRENT_UID=$(id -u):$(id -g) docker-compose --project-name query run --rm --name rawsql sqlraw
	@docker-compose --project-name query run --rm --name rawsql sqlraw

access:
	@docker exec -u root rawsql chmod 777 .

tag:
	@docker tag query_sqlraw:latest ichux/sqlraw:latest

upload:
	@docker login
	@docker push ichux/sqlraw:latest
