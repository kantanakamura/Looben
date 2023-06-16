container_name = looben_web

up: 
	docker-compose up

down:
	docker-compose down

build:
	docker-compoe build

exec:
	docker exec -it $(container_name) bash

pytest:
	docker exec -it $(container_name) bash -c "export DJANGO_SETTINGS_MODULE=Looben.settings && pytest"