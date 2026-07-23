# Evidencia - MLflow Tracking

Comando executado:

```powershell
$env:MLFLOW_TRACKING_URI='file:mlruns'; .\.venv\Scripts\python -m src.ml.train
```

Resultado validado:

```text
Trained rain prediction model: models\rain_model.joblib
MLflow run id: 26f62bb2b03542138a6a151a1c3f78e0
```

Observacao:

`models/` e `mlruns/` ficam ignorados pelo Git. Esta evidencia documenta a
execucao sem versionar artefatos pesados.
