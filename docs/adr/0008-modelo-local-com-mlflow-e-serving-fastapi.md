# ADR 0008 - Modelo local com MLflow e serving FastAPI

## Status

Aceita

## Contexto

O projeto precisa demonstrar integracao MLOps: treino de modelo, tracking de
experimentos, persistencia de artefato e serving por API. A solucao deve ser
simples de executar localmente e testavel no CI.

## Decisao

Implementar o treino em `src/ml/train.py` usando scikit-learn e MLflow.

O dataset de treino e derivado de `weather_daily.parquet`. O target
`will_rain_tomorrow` e calculado com base em `rain_sum` do dia seguinte para a
mesma cidade.

O modelo salvo fica em:

```text
models/rain_model.joblib
models/model_info.json
```

A API FastAPI expoe:

- `GET /model/info`;
- `POST /predict/rain`.

## Consequencias

Essa decisao completa o fluxo MLOps minimo: dados processados geram um modelo
versionavel, metricas sao rastreadas no MLflow e a predicao fica acessivel pela
API.

Quando o dataset possui duas ou mais classes, o treino usa
`RandomForestClassifier`. Quando o dataset e pequeno e possui apenas uma classe,
o treino usa `DummyClassifier` para manter a demonstracao funcional.

Se o servidor MLflow configurado nao estiver disponivel, o treino usa
`file:mlruns` como fallback local. Isso preserva o tracking mesmo sem o servico
MLflow via Compose rodando.
