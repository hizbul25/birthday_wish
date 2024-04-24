SHELL := /bin/bash # Use bash syntax
ARG := $(word 2, $(MAKECMDGOALS) )


# Commands for Docker version
install_project:
	@echo "Initializaing project...."
	@cp config/settings/local.py.example config/settings/local.py
	@cp .env.example .env


	@echo "Project initialized successfully."
	@docker volume create birthday_wisher_database
	@docker-compose build
	@echo "Docker setup complete."

	@echo "Starting Docker containers..."
	@docker-compose up -d
	@echo "Docker containers started."


	@echo "Running migrations"
	@docker-compose run --rm app python manage.py makemigrations
	@docker-compose run --rm app python manage.py migrate
	@echo "Creating superuser..."
	@docker-compose run --rm app python manage.py create_superuser
	@echo "Do you want to seed customer? (yes/no)"
	@read answer; \
	if [ "$$answer" = "yes" ]; then \
		echo "Seeding customers..."; \
		docker-compose run --rm app python manage.py customer_seeder; \
		echo "Customer seeded successfully."; \
	else \
		echo "Skipping seeders."; \
	fi
	@docker-compose run --rm app python manage.py collectstatic
	@echo "User 'admin' created. Default password is 'password'"
	@echo "Service URLs:"
	@echo "http://localhost:8000"



init_project:
	@cp config/settings/local.py.example config/settings/local.py
	@cp .env.example .env
	@cp .env.example .env

docker_setup:
	docker volume create birthday_wisher_database
	docker-compose build

docker_test:
	@cp .env.test .env
	docker-compose run --rm app python manage.py test customer
	@cp .env.example .env


docker_up:
	docker-compose up -d

docker_update_dependencies:
	docker-compose down --volumes
	docker-compose up -d --build

docker_down:
	docker-compose down --volumes

docker_logs:
	docker-compose logs -f $(ARG)

docker_makemigrations:
	docker-compose run --rm app python manage.py makemigrations

docker_migrate:
	docker-compose run --rm app python manage.py migrate

docker_create_superuser:
	docker-compose run --rm app python manage.py create_superuser

docker_seed_customer:
	docker-compose run --rm app python manage.py customer_seeder

docker_wish_birthday:
	docker-compose run --rm app python manage.py wish_birthday
