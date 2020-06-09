help:
	@echo "\`make <target>\` where <target> is one of"
	@echo "  build			build the image"
	@echo "  bash			to make bash for the docker environment"
	@echo "  access		to make the environment fit by changing the modes"

build:
	@docker-compose --project-name sqlraw build

bash:
	@docker-compose --project-name sqlraw run --rm --name co-sqlraw sqlraw

access:
	@docker exec -u root sqlraw chmod 777 .
