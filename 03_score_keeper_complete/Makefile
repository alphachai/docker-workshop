.DEFAULT_GOAL := help

CURRENT_VENV := $(shell python -c 'from __future__ import print_function; import sys; print(sys.prefix if hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix) else "", end="")')

ifeq ($(CURRENT_VENV),)
  VIRTUALENV := .venv
else
  VIRTUALENV := $(CURRENT_VENV)
endif

VENV_WORKDIR ?= .

ifeq ($(VENV_WORKDIR),.)
  PIPENV := PIPENV_VENV_IN_PROJECT=1 pipenv
else
  PIPENV := PIPENV_VENV_IN_PROJECT= WORKON_HOME='$(shell realpath $(VENV_WORKDIR))' pipenv
  # if the venv doesn't exist then this will fail, so it will make the VIRTUALENV will be empty
  VIRTUALENV := $(shell $(PIPENV) --venv 2> /dev/null)
  ifneq ($(.SHELLSTATUS),0)
    # means pipenv failed, so it doesn't exist yet. Need to cause a make env
    _ := $(shell $(value PIPENV) install --dev --deploy)
# .SHELLSTATUS requires Make 4.2 which isn't on Ubuntu or AMI yet, so the !=0 test always passes
#    ifneq ($(.SHELLSTATUS),0)
#      _ := $(error "Unable to install requirements")
#    endif
    VIRTUALENV := $(shell $(PIPENV) --venv 2> /dev/null)
  endif
endif

WITH_PIPENV := $(PIPENV) run

SERVICE_NAME := bloob
DOCKER_COMPOSE := docker-compose -p "$(SERVICE_NAME)_$(shell ls -id . | cut -d' ' -f1)_$(shell id -u)" -f docker/docker-compose.yml
CONTAINER_NAME := $(DOCKER_COMPOSE) ps | grep UP | grep -o -E "$(SERVICE_NAME)_[0-9]+_[0-9]+_$(SERVICE_NAME)_[a-z0-9_]+"

help:  ## print this help
	@# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Environment Variables:"
	@echo ""
	@echo "    VENV_WORKDIR:  Create the development virtualenv in this directory"
	@echo "    TAG:           Used with the 'build' and 'run' commands, changes the name of Docker image"
	@echo ""
.PHONY: help

env: $(VIRTUALENV) ## create development virtualenv
.PHONY: env
$(VIRTUALENV): $(VIRTUALENV)/bin/activate
$(VIRTUALENV)/bin/activate: Pipfile.lock
	$(PIPENV) install --dev --deploy
	if [ "$(VENV_WORKDIR)" = "." ]; then touch $(VIRTUALENV)/bin/activate; fi
Pipfile.lock: Pipfile
	$(PIPENV) lock

build: Pipfile.lock  ## build a Docker image of this Django project
	docker build . -f docker/Dockerfile -t "$${TAG:-$(SERVICE_NAME):latest}"
.PHONY: build

.env:
	@read -p "Enter a port for your dev site: " DJANGO_DEV_PORT; \
	echo "Dev settings (NOT FOR PRODUCTION USE!)" >> .env; \
	echo "DJANGO_DEBUG=true" >> .env; \
	echo "DJANGO_SECRET_KEY=foobar" >> .env; \
	echo "" >> .env; \
	echo "# Port for dev site. Must end in a colon (:)." >> .env; \
	echo "DJANGO_DEV_PORT=$$DJANGO_DEV_PORT:" >> .env; \
	echo "" >> .env; \
	echo "Wrote dev settings to .env" 1>&2; \

up: .env Pipfile.lock  ## run a dev site via docker-compose
	$(DOCKER_COMPOSE) up --build -d
.PHONY: up

up-tail: .env Pipfile.lock  ## run a dev site via docker-compose
	$(DOCKER_COMPOSE) up --build
.PHONY: up-tail

down: .env  ## tear down and delete the docker-compose dev site
	$(DOCKER_COMPOSE) down -v
.PHONY: down

start: up
.PHONY: start

stop: down
.PHONY: stop

restart: stop start  ## restart docker-compose dev site
.PHONY: restart

ps: .env  ## print docker-compose dev site container status
	$(DOCKER_COMPOSE) ps
.PHONY: ps

logs: .env  ## print logs from docker-compose dev site
	$(DOCKER_COMPOSE) logs
.PHONY: logs

tail: .env  ## tail logs from docker-compose dev site
	$(DOCKER_COMPOSE) logs -f
.PHONY: tail

exec: .env  ## exec bash into the service
	$(CONTAINER_NAME) | xargs -I % bash -c '</dev/tty docker exec -it % bash'
.PHONY: exec

clean: clean-pyc clean-venv clean-reports ## remove all build, test, coverage and Python artifacts
.PHONY: clean

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
.PHONY: clean-pyc

clean-venv: ## remove development virtualenv
	rm -rf $(VIRTUALENV)
.PHONY: clean-venv

clean-reports:  ## cleanup test JUnit and coverage reports
	rm -rf reports/
	rm -rf junit.xml junit-*.xml
	rm -rf coverage.xml .coverage .coverage.* *.cover
.PHONY: clean-reports

reports/:
	@mkdir reports

lint: $(VIRTUALENV) reports/
	touch reports/python.flake8
	#$(PIPENV) check
	$(WITH_PIPENV) flake8 --tee --exit-zero
	$(WITH_PIPENV) ./manage.py check

isort: $(VIRTUALENV) ## automatically sort Python imports
	$(WITH_PIPENV) isort
.PHONY: isort

test: $(VIRTUALENV)
	$(WITH_PIPENV) ./manage.py migrate
	$(WITH_PIPENV) ./manage.py test
.PHONY: test

test-post-build:
.PHONY: test-post-build

bump_release_number: $(VIRTUALENV) ## increment the release version number i.e. 1.0.0.rc0 -> 1.0.0.rc1
	@if [ "$$(  grep 'current_version.*dev[0-9]\+' .bumpversion.cfg )" ]; then echo 'cannot do release from dev version' && exit 1; fi
	$(PIPENV) run bumpversion release_number --tag --verbose
	git push
	git push --tags
.PHONY: bump_patch

bump_patch: $(VIRTUALENV) ## increment the patch version number i.e. 1.0.0.dev0 -> 1.0.1.dev0
	$(PIPENV) run bumpversion patch --verbose
.PHONY: bump_patch

bump_minor: $(VIRTUALENV) ## increment the minor version number i.e. 1.0.0.dev0 -> 1.1.0.dev0
	$(PIPENV) run bumpversion minor --verbose
.PHONY: bump_minor

bump_major: $(VIRTUALENV) ## increment the major version number i.e. 1.0.0.dev0 -> 2.0.0.dev0
	$(PIPENV) run bumpversion major --verbose
.PHONY: bump_major

release_candidate: $(VIRTUALENV) ## create a rc tag from the current dev version i.e. 1.0.0.dev0 -> 1.0.0.rc0
	@if [ ! "$$(  grep 'current_version.*dev[0-9]\+' .bumpversion.cfg )" ]; then echo 'the current version must be dev to promote to rc' && exit 1; fi
	@if [ "$$(git rev-parse --abbrev-ref HEAD 2>&1)" != "master" ]; then echo 'must be on master branch to release!' && exit 1; fi
	$(PIPENV) run bumpversion release --tag --verbose
	git push
	git push --tags
.PHONY: release_candidate

release: $(VIRTUALENV) ## create a release tag from the current dev version i.e. 1.0.0.dev0 -> 1.0.0
	@if [ ! "$$(  grep 'current_version.*rc[0-9]\+' .bumpversion.cfg )" ]; then echo 'the current version must be rc to promote to release' && exit 1; fi
	@if [ "$$(git rev-parse --abbrev-ref HEAD 2>&1)" != "master" ]; then echo 'must be on master branch to release!' && exit 1; fi
	$(PIPENV) run bumpversion release --tag --verbose
	git push
	git push --tags
.PHONY: release
