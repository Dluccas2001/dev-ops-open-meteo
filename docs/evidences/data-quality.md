# Evidencia - Data Quality

Comandos executados:

```powershell
$env:DATA_RAW_DIR='data/samples'; $env:DATA_PROCESSED_DIR='data/processed'; .\.venv\Scripts\python -m src.jobs.transform
$env:DATA_PROCESSED_DIR='data/processed'; .\.venv\Scripts\python -m src.quality.checks
```

Resultado validado:

```text
Saved processed hourly dataset: data\processed\weather_hourly.parquet
Saved processed daily dataset: data\processed\weather_daily.parquet
Data quality checks passed for processed weather datasets.
```
