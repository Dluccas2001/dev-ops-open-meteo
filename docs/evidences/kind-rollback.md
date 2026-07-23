# Evidencia - Kind Rollback

Status:

```text
Pendente de execucao no WSL do usuario.
```

Comandos para executar no WSL:

```bash
kubectl rollout history deployment/weather-api -n weather-mlops
kubectl rollout restart deployment/weather-api -n weather-mlops
kubectl rollout status deployment/weather-api -n weather-mlops
kubectl rollout undo deployment/weather-api -n weather-mlops
kubectl rollout status deployment/weather-api -n weather-mlops
```

Depois de executar, cole neste arquivo o output real.
