# Evidencia - Carga PostgreSQL

Comando executado:

```powershell
docker compose exec -T api python -m src.jobs.load
```

Resultado validado:

```text
Loaded processed datasets into tables: weather_hourly, weather_daily
```

Database usada:

```text
open-meteo
```
