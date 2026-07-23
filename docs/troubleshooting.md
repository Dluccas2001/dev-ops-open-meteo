# Troubleshooting

## Docker no WSL nao encontra daemon

Sintoma:

```text
The command 'docker' could not be found in this WSL 2 distro
```

Solucao:

- abrir Docker Desktop no Windows;
- ativar integracao com a distro em `Settings > Resources > WSL Integration`;
- rodar `wsl --shutdown`;
- abrir o WSL novamente e testar `docker run hello-world`.

## Postgres do Compose falha por senha ausente

Sintoma:

```text
Database is uninitialized and superuser password is not specified
```

Solucao:

Garantir no `.env` local:

```env
POSTGRES_DB=open-meteo
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua-senha-local
```

## API no Compose nao conecta ao Postgres

Dentro do Docker Compose, `localhost` aponta para o proprio container da API. O
host correto do banco e o nome do servico:

```env
DB_HOST=postgres
```

Para rodar Python direto na maquina, use:

```env
DB_HOST=localhost
```

## Imagem nao encontrada no Kind

Sintoma:

```text
ERROR: image: "weather-mlops-api:local" not present locally
```

Solucao:

```bash
docker build -f ContainerFile -t weather-mlops-api:local .
kind load docker-image weather-mlops-api:local --name weather-mlops
```

## kubectl nao encontra cluster

Sintoma:

```text
Unable to connect to the server: dial tcp [::1]:8080
```

Solucao:

Verificar o contexto no mesmo ambiente onde o Kind foi criado:

```bash
kind get clusters
kubectl config current-context
kubectl get nodes
```

Se o cluster foi criado no WSL, rode `kubectl` no WSL.

## Modelo nao encontrado

Sintoma:

```text
Rain prediction model is unavailable. Run train job first.
```

Solucao:

```bash
python -m src.ml.train
```

ou, no Compose:

```bash
docker compose exec -T api python -m src.ml.train
```

No Kind, gere os datasets e o modelo dentro do pod:

```bash
kubectl exec -n weather-mlops deployment/weather-api -- sh -c "DATA_RAW_DIR=/app/data/samples DATA_PROCESSED_DIR=/app/data/processed python -m src.jobs.transform && DATA_PROCESSED_DIR=/app/data/processed python -m src.quality.checks && DATA_PROCESSED_DIR=/app/data/processed MLFLOW_TRACKING_URI=file:/app/mlruns python -m src.ml.train"
```

Depois teste novamente:

```bash
curl http://localhost:8001/model/info
```

## Data quality falha

Sintoma:

```text
pandera.errors.SchemaError
```

Solucao:

```bash
python -m src.jobs.transform
python -m src.quality.checks
```

## CI falha no Ruff format

Sintoma:

```text
Would reformat ...
```

Solucao:

```bash
python -m ruff format .
python -m ruff check .
```
