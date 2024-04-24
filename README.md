# Birthday Wisher Documentation

### Setup

- Clone the project on your machine:
  - Please make sure docker in running in your machine.
  - In your preferred directory `git clone -b develop https://github.com/hizbul25/birthday_wish.git`
  - Navigate into the project `cd birthday_wish`
  - Single command installation: `make install_project`

### Step by step installation:

- Open a new command line window and go to the project's directory
- Prepare project :
  `make init_project`
- Run the initial setup:
  `make docker_setup`
- Run the project:
  `make docker_up`
- Run migrations: `make docker_makemigrations && docker_migrate`
- Collect static: `docker-compose run --rm app python manage.py collectstatic`
- Run seeders:

  - `make docker_create_superuser` Creates a superuser with the username: _admin_ and password: _password_. Use these credentials to log in to the admin panel, where you can view customers, and API endpoints.
  - `make docker_seed_customer` Creates 100 Customer

- Access (http://localhost:8000) in your browser; the project should be running there.
  - When you run make docker_up, various containers are spun up (app, database, redis, celery, etc.), each running on a different port.
  - To install dependencies use: `make docker_update_dependencies`
  - To chekc logs: `make docker_logs app` or `make docker_logs celery`
  - To stop the container: `make docker_down`

## Tools

- [Django as a backend framework](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery for background task queue](https://docs.celeryq.dev/en/stable/index.html)
- [Redis for caching and broker](https://redis.io/)
- [Gunicorn HTTP Server for UNIX](https://gunicorn.org/)
- [PostgreSQL Database Adapter](https://pypi.org/project/psycopg2-binary/)
- [Faker for seeding data](https://faker.readthedocs.io/en/master/)

### Testing

Just run: `make docker_test`

### Send Birthday Wish

#### Manually

- run: `make docker_wish_birthday {date}`
- Example: `make docker_wish_birthday '04-24'`

#### Schedule

- Celery task schedular will send wish to customer everyday at 9:00 AM, You can update it from `.env.example` file

- To check mail send: check celery log by running `make docker_logs celery`
- You may get log from `report.log` file.

### API Endpoint

- Create customer: `http://localhost:8000/api/v1/customer/register/`
- Listing customer: `http://localhost:8000/api/v1/customer/`
