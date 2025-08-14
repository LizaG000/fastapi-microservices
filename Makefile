compose:
	docker compose -f ./deploy/docker-compose.yml up --build -d
	docker exec -it deploy-user_microservice-1 alembic -c user_microservice/alembic.ini upgrade head
	docker exec -it deploy-task_microservice-1 alembic -c task_microservice/alembic.ini upgrade head

down:
	docker compose -f deploy/docker-compose.yml down

migrations_init_user:
	docker exec -it deploy-user_microservice-1 alembic -c user_microservice/alembic.ini revision --autogenerate -m "init"

makemigrations_user:
	docker exec -it deploy-user_microservice-1 alembic -c user_microservice/alembic.ini revision --autogenerate -m "$(MSG)"

migrate_user:
	docker exec -it deploy-user_microservice-1 alembic -c user_microservice/alembic.ini upgrade head

downgrade_user:
	docker exec -it deploy-user_microservice-1 alembic -c user_microservice/alembic.ini downgrade -1

migrations_init_task:
	docker exec -it deploy-task_microservice-1 alembic -c task_microservice/alembic.ini revision --autogenerate -m "init"

makemigrations_task:
	docker exec -it deploy-task_microservice-1 alembic -c task_microservice/alembic.ini revision --autogenerate -m "$(MSG)"

migrate_task:
	docker exec -it deploy-task_microservice-1 alembic -c task_microservice/alembic.ini upgrade head

downgrade_task:
	docker exec -it deploy-task_microservice-1 alembic -c task_microservice/alembic.ini downgrade -1