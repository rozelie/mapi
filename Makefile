#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`

#* Docker variables
IMAGE := mapi
VERSION := latest

#* Formatters
.PHONY: format
format:
	isort --settings-path pyproject.toml ./
	black --config pyproject.toml ./

#* Docker
# Example: make docker-build VERSION=latest
# Example: make docker-build IMAGE=some_name VERSION=0.1.0
.PHONY: docker-build
docker-build:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make docker-remove VERSION=latest
# Example: make docker-remove IMAGE=some_name VERSION=0.1.0
.PHONY: docker-remove
docker-remove:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)
