# Evidencia - Endpoint de Predicao

Endpoint:

```text
POST /predict/rain
```

Payload usado:

```json
{
  "city": "sao-paulo",
  "temp_mean": 22.0,
  "temp_min": 18.0,
  "temp_max": 26.0,
  "humidity_mean": 75.0,
  "wind_mean": 9.0,
  "rain_sum": 0.0,
  "month": 7,
  "day_of_week": 0
}
```

Resultado validado:

```text
city: sao-paulo
will_rain_tomorrow: False
probability: 0.0
model_version: local
```

Endpoint de metadados do modelo tambem validado:

```text
GET /model/info
model_version: local
features: temp_mean, temp_min, temp_max, humidity_mean, wind_mean, rain_sum, month, day_of_week, city, region
```
