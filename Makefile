help:
	@echo "\`make <target>\` where <target> is one of"
	@echo "  build			build the image"
	@echo "  tag			tags the image"
	@echo "  upload		uploads to docker hub"

build: clean
	@docker-compose --project-name query up --build -d
	@make tag

tag:
	@docker tag query_sqlraw:latest ichux/sqlraw:latest

upload:
	@docker login
	@docker push ichux/sqlraw:latest
