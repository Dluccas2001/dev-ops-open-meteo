# Evidencia - Docker Compose

Comandos executados:

```powershell
docker compose up -d --build
docker compose ps
```

Resultado validado:

```text
weather_mlops_api        Up
weather_mlops_mlflow     Up
weather_mlops_postgres   Up (healthy)
```

Revalidacao local:

```text
weather_mlops_api        Up 13 minutes
weather_mlops_mlflow     Up 28 minutes
weather_mlops_postgres   Up 13 minutes (healthy)
```

Endpoints testados:

```text
GET /health
GET /metadata
GET /cities
GET /weather/summary
GET /weather/latest?city=sao-paulo
POST /predict/rain
```

Respostas revalidadas:

```text
/health: healthy
/weather/summary: cities=1, days=2, rainy_days=1, avg_temp_mean=20.0
/model/info: model_version=local
```
