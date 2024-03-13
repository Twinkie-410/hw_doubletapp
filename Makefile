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

check_lint:
	isort --check --diff .
	flake8 --config setup.cfg
	black --check --config pyproject.toml .

#docker
REGISTRY=gitlab.com
GROUP=test-assignment
PROJECT=doubletapp
build: ## Build the container
	docker build -t $(REGISTRY)/$(GROUP)/$(PROJECT)/$(APP_NAME) .
push:
    docker push $(REGISTRY)/$(GROUP)/$(PROJECT)/$(APP_NAME):latest

build-nc: ## Build the container without caching
	docker build --no-cache -t $(APP_NAME) .

run:
	docker run -i -t --rm -p=$(PORT):$(PORT) --name="$(APP_NAME)" $(APP_NAME)

stop: ## Stop and remove a running container
	docker stop $(APP_NAME); docker rm $(APP_NAME)

#docker compose
compose-build:
        docker compose -f docker compose.yml build $(c)
compose-up:
        docker compose -f docker compose.yml up -d $(c)
compose-start:
        docker compose -f docker compose.yml start $(c)
compose-down:
        docker compose -f docker compose.yml down $(c)
compose-stop:
        docker compose -f docker compose.yml stop $(c)
compose-restart:
        docker compose -f docker compose.yml stop $(c)
        docker compose -f docker compose.yml up -d $(c)
compose-ps:
        docker compose -f docker compose.yml ps



