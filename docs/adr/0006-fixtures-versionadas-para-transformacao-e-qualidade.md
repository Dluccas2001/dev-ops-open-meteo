# ADR 0006 - Fixtures versionadas para transformacao e qualidade

## Status

Aceita

## Contexto

O CI precisa validar transformacao e data quality sem depender da disponibilidade
da API Open-Meteo. Ao mesmo tempo, os testes devem representar o formato real dos
arquivos raw gerados pela ingestao.

## Decisao

Manter uma fixture raw pequena e versionada em `data/samples/open_meteo`.

O workflow de CI usa essa amostra para:

- executar `src.jobs.transform`;
- gerar `weather_hourly.parquet` e `weather_daily.parquet`;
- executar `src.quality.checks` sobre os Parquets gerados.

## Consequencias

Essa decisao torna o CI deterministico e rapido, mantendo cobertura sobre o
contrato real `raw -> processed -> quality`.

A fixture precisa ser atualizada se o formato do raw storage mudar. Essa
responsabilidade e pequena e explicita, e evita que testes chamem a internet.
