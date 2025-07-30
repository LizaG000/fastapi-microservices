compose:
	docker compose -f deploy/docker-compose.yml up --build -d

down:
	docker compose -f deploy/docker-compose.yml down

migrations_init:
	docker exec -it deploy-user_microservice-1 alembic revision --autogenerate -m "init"

migrate:
	docker exec -it deploy-user_microservice-1 alembic -c user_microservice/alembic.ini upgrade head

downgrade:
	docker exec -it deploy-user_microservice-1 alembic -c user_microservice/alembic.ini downgrade -1
