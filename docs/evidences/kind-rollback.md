# Evidencia - Kind Rollback

Status:

```text
Validado no WSL do usuario.
```

Comandos executados:

```bash
kubectl rollout history deployment/weather-api -n weather-mlops
kubectl rollout restart deployment/weather-api -n weather-mlops
kubectl rollout status deployment/weather-api -n weather-mlops
kubectl rollout undo deployment/weather-api -n weather-mlops
kubectl rollout status deployment/weather-api -n weather-mlops
```

Historico do deployment:

```text
deployment.apps/weather-api
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>
```

Restart validado:

```text
deployment.apps/weather-api restarted
deployment "weather-api" successfully rolled out
```

Rollback validado:

```text
deployment.apps/weather-api rolled back
deployment "weather-api" successfully rolled out
```

Observacao:

O `kubectl rollout undo` exibiu um aviso informando que o recurso tinha sido
gerenciado previamente com `kubectl apply`. Esse aviso e esperado nesse fluxo de
demo local e nao impediu o rollback.
