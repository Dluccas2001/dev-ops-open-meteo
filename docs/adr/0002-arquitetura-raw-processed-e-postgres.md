# ADR 0002 - Arquitetura raw, processed e PostgreSQL

## Status

Aceita

## Contexto

O projeto precisa evidenciar boas praticas de engenharia de dados: preservar dados
brutos, transformar dados de forma reprodutivel, validar qualidade e disponibilizar
dados para consulta via API.

Tambem e necessario manter uma arquitetura simples o suficiente para ser executada
localmente durante a demonstracao.

## Decisao

Organizar os dados em tres camadas principais:

- `data/raw/open_meteo/{city}/{run_date}.json` para armazenar respostas brutas da
  Open-Meteo.
- `data/processed/weather_hourly.parquet` e
  `data/processed/weather_daily.parquet` para datasets tratados.
- PostgreSQL para persistir os dados processados e servir consultas da API.

Na primeira entrega, os arquivos raw e processed ficarao no filesystem local. O
uso de armazenamento objeto, como S3 local, fica fora do escopo inicial.

## Consequencias

A camada raw permite reprocessamento sem nova chamada a API externa. A camada
processed em Parquet facilita leitura analitica e treino de modelo. O PostgreSQL
aproxima o projeto de uma arquitetura operacional real e permite criar endpoints
de consulta com filtros por cidade e data.

O uso de filesystem local simplifica a operacao, mas exige cuidado com `.gitignore`
para evitar versionar dados gerados.
