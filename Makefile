compose:
	docker compose -f deploy/docker-compose.yml up --build -d

down:
	docker compose -f deploy/docker-compose.yml down

migrations_init:
	 alembic revision --autogenerate -m "init"

migrate:
	docker exec -i deploy-user_microservice-1 alembic -c user_microservice/alembic.ini upgrade head

downgrade:
	docker exec -i deploy-user_microservice-1 alembic -c user_microservice/alembic.ini downgrade -1
