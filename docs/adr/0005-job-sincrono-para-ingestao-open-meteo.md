# ADR 0005 - Job sincrono para ingestao Open-Meteo

## Status

Aceita

## Contexto

A primeira etapa funcional do pipeline precisa coletar dados da Open-Meteo e
persistir respostas brutas em disco. A implementacao deve ser simples de executar
localmente, facil de testar no CI e adequada para evoluir depois para orquestracao
ou execucao em Kubernetes.

## Decisao

Implementar a ingestao como um job Python sincrono em `src/jobs/ingest.py`.

O job:

- le as cidades versionadas em `config/cities.yaml`;
- monta parametros da API a partir de latitude, longitude, timezone e variaveis
  climaticas escolhidas;
- usa `requests` para chamar a Open-Meteo;
- salva um JSON raw por cidade e data em
  `data/raw/open_meteo/{city}/{YYYY-MM-DD}.json`;
- inclui metadados de origem, cidade e horario de ingestao junto da resposta da
  API.

## Consequencias

Essa abordagem reduz a complexidade inicial e atende ao requisito de ingestao de
API para raw storage. As funcoes foram separadas para permitir testes unitarios
com mock da chamada HTTP, mantendo o CI independente da internet.

A limitacao e que a execucao ainda e sequencial. Caso o numero de cidades cresca,
poderemos evoluir para paralelismo controlado ou orquestracao com uma ferramenta
como Airflow ou Dagster.
