# dev-ops-open-meteo

Pipeline de dados climaticos com DevOps e MLOps usando a API publica Open-Meteo.

> Status atual: scaffold inicial configurado, API minima funcionando, Ruff verde e testes unitarios passando.

## Objetivo

Este projeto demonstra um fluxo completo de Engenharia de Dados e MLOps:

- ingestao de dados da Open-Meteo;
- persistencia em camada raw;
- transformacao para datasets processados;
- data quality;
- carga em PostgreSQL;
- API FastAPI;
- treinamento e tracking com MLflow;
- serving de modelo;
- CI/CD;
- operacao local em Kubernetes com Kind.

## Status

Fase atual: **Fase 1 - Scaffold e ambiente**.

Ja configurado:

- estrutura inicial de pastas;
- ambiente Python com dependencias;
- FastAPI minima;
- endpoints `/health` e `/metadata`;
- testes unitarios iniciais;
- Ruff para lint/format;
- Compose preparado para API, PostgreSQL e MLflow;
- CI inicial no GitHub Actions;
- plano completo em `PLANO_IMPLEMENTAÇÃO.md`.

## Requisitos

- Python 3.11 ou 3.12
- Git
- Docker ou Podman
- Docker Compose ou Podman Compose
- Make ou PowerShell
- kubectl
- Kind
- Trivy

Para a primeira fase, apenas Python e Git ja permitem rodar a API e os testes. Docker, kubectl, Kind e Trivy entram nas proximas fases.

Veja detalhes em [docs/ambiente.md](docs/ambiente.md).

## Setup Local Com zsh, WSL Ou Git Bash

Em ambientes Linux-like, o comando pode ser `python3` antes do ambiente virtual existir.

Entre na pasta do projeto:

```bash
cd "/mnt/h/Projetos/DevOps e MLOps/dev-ops-open-meteo"
```

Verifique a versao:

```bash
python3 --version
```

Crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Depois que o `.venv` estiver ativo, use `python` normalmente:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Crie o arquivo de configuracao local:

```bash
cp .env.example .env
```

## Setup Local Com PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Se a execucao de scripts PowerShell estiver bloqueada, voce pode usar os comandos Python acima diretamente. O script auxiliar tambem existe:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1 setup
```

## Validar Instalacao

Com o `.venv` ativo, rode:

```bash
python -m ruff check .
python -m pytest
```

Resultado esperado:

```text
All checks passed!
2 passed
```

## Rodar API Local

Com o `.venv` ativo:

```bash
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse:

```text
http://localhost:8000/docs
http://localhost:8000/health
http://localhost:8000/metadata
```

Observacao: `GET /` ainda retorna `404 Not Found`, porque a raiz da API ainda nao foi implementada. Por enquanto os endpoints validos sao `/health`, `/metadata` e `/docs`.

Para parar a API:

```text
Ctrl + C
```

## Comandos Uteis

```bash
python -m ruff check .
python -m ruff check . --fix
python -m pytest
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Com Make instalado, os equivalentes serao:

```bash
make lint
make test
make run-api
```

Enquanto `make` nao estiver disponivel no Windows, use os comandos `python -m ...`.

## Docker E Servicos Locais

O arquivo `compose.yaml` ja esta preparado para subir:

- `api`;
- `postgres`;
- `mlflow`.

Quando Docker Desktop ou Podman estiver instalado:

```bash
docker compose up -d --build
docker compose down
```

## Proximas Ferramentas A Instalar

Para as fases seguintes:

```powershell
winget install Docker.DockerDesktop
winget install Kubernetes.kubectl
winget install Kubernetes.kind
winget install AquaSecurity.Trivy
```

Depois validar:

```powershell
docker --version
docker compose version
kubectl version --client
kind version
trivy --version
```

## Plano

O plano completo esta em [PLANO_IMPLEMENTAÇÃO.md](PLANO_IMPLEMENTAÇÃO.md).

## Proximos Passos De Implementacao

1. Implementar ingestao real da Open-Meteo.
2. Salvar JSON raw por cidade e data.
3. Transformar raw em datasets Parquet hourly e daily.
4. Adicionar checks de data quality com Pandera.
5. Carregar PostgreSQL.
6. Evoluir API de consulta.
7. Treinar modelo e registrar no MLflow.
