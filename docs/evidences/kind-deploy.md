# Evidencia - Kind Deploy

Status:

```text
Pendente de execucao no WSL do usuario.
```

Motivo:

O cluster Kind foi criado no WSL. O `kubectl` executado pelo PowerShell nao
enxerga esse contexto e tentou conectar em `localhost:8080`.

Comandos para executar no WSL:

```bash
kind load docker-image weather-mlops-api:local --name weather-mlops
kubectl apply -k k8s
kubectl get all -n weather-mlops
kubectl rollout status deployment/weather-api -n weather-mlops
```

Depois de executar, cole neste arquivo o output real.
