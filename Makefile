migrate:
	python src/manage.py migrate $(if $m, api $m,)

makemigrations:
	python src/manage.py makemigrations
	sudo chown -R ${USER} src/app/migrations/

createsuperuser:
	python src/manage.py createsuperuser

collectstatic:
	python src/manage.py collectstatic --no-input

dev:
	python src/manage.py runserver localhost:8000

command:
	python src/manage.py ${c}

shell:
	python src/manage.py shell

debug:
	python src/manage.py debug

piplock:
	pipenv install
	sudo chown -R ${USER} Pipfile.lock

lint:
	isort .
	flake8 --config setup.cfg
	black --config pyproject.toml .
#
#check_lint:
#	isort --check --diff .
#	flake8 --config setup.cfg
#	black --check --config pyproject.toml .
#lint:
#	docker-compose run django isort --check --diff .
#	docker-compose run django flake8 --config setup.cfg
#	docker-compose run django black --check --config pyproject.toml .
#	docker-compose down

test:
	echo success

#docker
#to-do pull
REGISTRY=registry.gitlab.com/test-assignment2273206/doubletapp
#GROUP=test-assignment
#PROJECT=doubletapp
APP_NAME=hw_doubletapp
build: ## Build the container
	docker build -t $(REGISTRY)/$(APP_NAME) .
push:
	docker push $(REGISTRY)/$(APP_NAME):latest

pull:
	docker pull $(REGISTRY)/$(APP_NAME):latest
build-nc: ## Build the container without caching
	docker build --no-cache -t $(REGISTRY)/$(APP_NAME) .

run:
	docker run -i -t --rm -p=$(PORT):$(PORT) --name="$(APP_NAME)" $(APP_NAME)

stop: ## Stop and remove a running container
	docker stop $(APP_NAME); docker rm $(APP_NAME)

#docker compose
compose-build:
	docker compose build -f docker-compose.yml $(c)
compose-up:
	docker compose up -f docker-compose.yml -d $(c)
compose-start:
	docker compose start -f docker-compose.yml $(c)
compose-down:
	docker compose down $(c)
compose-stop:
	docker compose stop -f docker-compose.yml $(c)
compose-restart:
	docker compose stop -f docker-compose.yml $(c)
	docker compose up -f docker-compose.yml -d $(c)
compose-ps:
	docker compose ps -f docker-compose.yml

deploy:
	docker compose -f docker-compose.yml up $(c) -d
	#echo "There will be real deploy here sometime"
