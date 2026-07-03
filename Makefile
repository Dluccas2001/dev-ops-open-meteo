.PHONY: help setup lint format test quality build scan up down logs run-api ingest transform load train pipeline validate-k8s kind-create kind-delete deploy status rollback clean
.DEFAULT_GOAL := help

PYTHON ?= python
COMPOSE ?= docker compose
IMAGE_NAME ?= weather-mlops-api
IMAGE_TAG ?= local
KIND_CLUSTER ?= weather-mlops
K8S_NAMESPACE ?= weather-mlops

help: ## Mostra os comandos disponiveis
	@echo "Uso: make [alvo]"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Cria ambiente virtual e instala dependencias
	$(PYTHON) -m venv .venv
	.venv/Scripts/python -m pip install --upgrade pip
	.venv/Scripts/python -m pip install -r requirements-dev.txt

lint: ## Executa lint com Ruff
	$(PYTHON) -m ruff check .

format: ## Formata codigo com Ruff
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check . --fix

test: ## Executa testes automatizados
	$(PYTHON) -m pytest

quality: ## Executa data quality checks
	$(PYTHON) -m src.quality.checks

build: ## Constroi imagem da API
	docker build -f ContainerFile -t $(IMAGE_NAME):$(IMAGE_TAG) .

scan: ## Executa scan com Trivy
	trivy image --severity HIGH,CRITICAL $(IMAGE_NAME):$(IMAGE_TAG)

up: ## Sobe ambiente local via Compose
	$(COMPOSE) up -d --build

down: ## Derruba ambiente local
	$(COMPOSE) down

logs: ## Mostra logs do Compose
	$(COMPOSE) logs -f

run-api: ## Roda API local sem container
	$(PYTHON) -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

ingest: ## Coleta dados da Open-Meteo
	$(PYTHON) -m src.jobs.ingest

transform: ## Transforma raw JSON em datasets processados
	$(PYTHON) -m src.jobs.transform

load: ## Carrega dados no PostgreSQL
	$(PYTHON) -m src.jobs.load

train: ## Treina modelo e registra experimento
	$(PYTHON) -m src.ml.train

pipeline: ingest transform quality load train ## Executa pipeline local completo

validate-k8s: ## Valida manifests Kubernetes
	kubectl kustomize k8s

kind-create: ## Cria cluster Kind local
	kind create cluster --name $(KIND_CLUSTER)

kind-delete: ## Remove cluster Kind local
	kind delete cluster --name $(KIND_CLUSTER)

deploy: build ## Faz deploy local no Kind
	kind load docker-image $(IMAGE_NAME):$(IMAGE_TAG) --name $(KIND_CLUSTER)
	kubectl apply -k k8s

status: ## Mostra status no Kubernetes
	kubectl get all -n $(K8S_NAMESPACE)

rollback: ## Executa rollback da API no Kubernetes
	kubectl rollout undo deployment/weather-api -n $(K8S_NAMESPACE)

clean: ## Remove artefatos locais gerados
	$(PYTHON) scripts/clean_outputs.py

