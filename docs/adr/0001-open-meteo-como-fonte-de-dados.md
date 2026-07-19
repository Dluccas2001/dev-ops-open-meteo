# ADR 0001 - Open-Meteo como fonte de dados

## Status

Aceita

## Contexto

O projeto precisa demonstrar um pipeline de dados end-to-end para a disciplina de
DevOps e MLOps aplicada a Engenharia de Dados. A fonte escolhida deve permitir
ingestao automatizada, transformacao, validacao de qualidade, carga em banco,
treinamento de modelo e demonstracao em ambiente local.

Foram considerados datasets maiores, como bases completas de CNPJ, mas esse tipo
de fonte aumenta o risco operacional por volume, tempo de processamento e
complexidade de preparacao.

## Decisao

Usar a API publica Open-Meteo como fonte inicial de dados climaticos.

O endpoint inicial sera o de previsao, coletando variaveis horarias como:

- `temperature_2m`
- `relative_humidity_2m`
- `precipitation`
- `wind_speed_10m`

As cidades iniciais serao capitais brasileiras configuradas em
`config/cities.yaml`.

## Consequencias

Esta decisao reduz a complexidade de acesso aos dados, pois a API nao exige chave
de autenticacao e retorna JSON estruturado. O dataset tambem e adequado para
criar features climaticas, agregacoes diarias e um modelo simples para prever se
vai chover no dia seguinte.

A principal limitacao e que o projeto passa a depender da disponibilidade da API
externa para novas ingestoes. Para reduzir esse risco no CI, os testes devem usar
mocks ou fixtures locais.
