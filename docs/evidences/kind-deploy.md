# Evidencia - Kind Deploy

Status:

```text
Validado no WSL do usuario.
```

Comandos executados:

```bash
docker build -f ContainerFile -t weather-mlops-api:local .
kind load docker-image weather-mlops-api:local --name weather-mlops
kubectl apply -k k8s
kubectl rollout restart deployment/weather-api -n weather-mlops
kubectl rollout status deployment/weather-api -n weather-mlops
kubectl get all -n weather-mlops
kubectl port-forward -n weather-mlops service/weather-api 8001:8000
curl http://localhost:8001/health
```

Resultado do deploy:

```text
deployment "weather-api" successfully rolled out
```

Status dos recursos:

```text
pod/weather-api-7f48b46bc6-l9wll   1/1     Running     0
pod/weather-ingest-2tl2q           0/1     Completed   0

service/weather-api                ClusterIP   8000/TCP
deployment.apps/weather-api        1/1         1            1
job.batch/weather-ingest           Complete    1/1
```

Resposta do health check no Kind:

```json
{
  "status": "healthy",
  "app": "weather-mlops-pipeline",
  "environment": "kind"
}
```

Bootstrap de dados, qualidade e modelo dentro do pod:

```bash
kubectl exec -n weather-mlops deployment/weather-api -- sh -c "DATA_RAW_DIR=/app/data/samples DATA_PROCESSED_DIR=/app/data/processed python -m src.jobs.transform && DATA_PROCESSED_DIR=/app/data/processed python -m src.quality.checks && DATA_PROCESSED_DIR=/app/data/processed MLFLOW_TRACKING_URI=file:/app/mlruns python -m src.ml.train"
```

Resultado validado:

```text
Saved processed hourly dataset: /app/data/processed/weather_hourly.parquet
Saved processed daily dataset: /app/data/processed/weather_daily.parquet
Data quality checks passed for processed weather datasets.
Trained rain prediction model: /app/models/rain_model.joblib
MLflow tracking URI: file:/app/mlruns
MLflow run id: 0a99dcd7d95a4e50829cbb3d6e57493e
```

Observacao:

O MLflow avisou que o executavel `git` nao esta no PATH do container, entao o SHA
do Git nao foi registrado no run. Isso nao bloqueia o treino nem o serving.

Endpoint `/model/info`:

```json
{
  "model_path": "/app/models/rain_model.joblib",
  "model_version": "local",
  "metrics": {
    "accuracy": 1.0,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  }
}
```

Endpoint `/predict/rain`:

```json
{
  "city": "sao-paulo",
  "will_rain_tomorrow": false,
  "probability": 0.0,
  "model_version": "local"
}
```
