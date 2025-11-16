.SILENT:

# Default variables
PROFILE ?= dev
ENV_FILE ?= .env
COMPOSE ?= docker compose --env-file $(ENV_FILE)
CONTAINER ?= $(if $(filter prod,$(PROFILE)),api,api-dev) # Dynamically set container based on profile
SHELL_CMD ?= bash
OPTIONS ?= -u root

# Compose profile flags
PROFILE_FLAG = --profile $(PROFILE)

# Docker Compose commands
run:
	$(COMPOSE) $(PROFILE_FLAG) up -d --build

build:
	$(COMPOSE) $(PROFILE_FLAG) build --no-cache

stop:
	$(COMPOSE) $(PROFILE_FLAG) stop

down:
	$(COMPOSE) $(PROFILE_FLAG) down

logs:
	$(COMPOSE) $(PROFILE_FLAG) logs -f $(CONTAINER)

logs-all:
	$(COMPOSE) $(PROFILE_FLAG) logs -f

restart:
	$(COMPOSE) $(PROFILE_FLAG) restart $(CONTAINER)

shell:
	$(COMPOSE) $(PROFILE_FLAG) exec $(OPTIONS) $(CONTAINER) $(SHELL_CMD)

shell-root:
	$(MAKE) shell OPTIONS="-u root"

ps:
	$(COMPOSE) $(PROFILE_FLAG) ps

# Alembic migrations (assume alembic is inside CONTAINER)
migration:
	$(COMPOSE) $(PROFILE_FLAG) exec $(OPTIONS) $(CONTAINER) alembic revision --autogenerate -m "$(message)"

migration-upgrade:
	$(COMPOSE) $(PROFILE_FLAG) exec $(OPTIONS) $(CONTAINER) alembic upgrade head

migration-downgrade:
	$(COMPOSE) $(PROFILE_FLAG) exec $(OPTIONS) $(CONTAINER) alembic downgrade -1

migration-current:
	$(COMPOSE) $(PROFILE_FLAG) exec $(OPTIONS) $(CONTAINER) alembic current

migration-history:
	$(COMPOSE) $(PROFILE_FLAG) exec $(OPTIONS) $(CONTAINER) alembic history

# Python requirements
pip-list:
	$(COMPOSE) $(PROFILE_FLAG) exec $(OPTIONS) $(CONTAINER) pip list

# Examples of switching profiles
run-dev:
	$(MAKE) run PROFILE=dev

run-prod:
	$(MAKE) run PROFILE=prod

build-dev:
	$(MAKE) build PROFILE=dev

build-prod:
	$(MAKE) build PROFILE=prod

stop-dev:
	$(MAKE) stop PROFILE=dev

stop-prod:
	$(MAKE) stop PROFILE=prod

down-dev:
	$(MAKE) down PROFILE=dev

down-prod:
	$(MAKE) down PROFILE=prod

logs-dev:
	$(MAKE) logs PROFILE=dev

logs-prod:
	$(MAKE) logs PROFILE=prod

restart-dev:
	$(MAKE) restart PROFILE=dev

restart-prod:
	$(MAKE) restart PROFILE=prod

shell-dev:
	$(MAKE) shell PROFILE=dev

shell-prod:
	$(MAKE) shell PROFILE=prod

ps-dev:
	$(MAKE) ps PROFILE=dev

ps-prod:
	$(MAKE) ps PROFILE=prod

migration-dev:
	$(MAKE) migration PROFILE=dev message="$(message)"

migration-prod:
	$(MAKE) migration PROFILE=prod message="$(message)"

migration-dev-upgrade:
	$(MAKE) migration-upgrade PROFILE=dev

migration-prod-upgrade:
	$(MAKE) migration-upgrade PROFILE=prod

migration-dev-downgrade:
	$(MAKE) migration-downgrade PROFILE=dev

migration-prod-downgrade:
	$(MAKE) migration-downgrade PROFILE=prod

migration-dev-current:
	$(MAKE) migration-current PROFILE=dev

migration-prod-current:
	$(MAKE) migration-current PROFILE=prod

migration-dev-history:
	$(MAKE) migration-history PROFILE=dev

migration-prod-history:
	$(MAKE) migration-history PROFILE=prod

pip-list-dev:
	$(MAKE) pip-list PROFILE=dev

pip-list-prod:
	$(MAKE) pip-list PROFILE=prod
