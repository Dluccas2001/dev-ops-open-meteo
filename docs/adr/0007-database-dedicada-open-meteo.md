# ADR 0007 - Database dedicada open-meteo

## Status

Aceita

## Contexto

O ambiente local ja possui uma database PostgreSQL chamada `postgres`, usada por
outro projeto. Misturar tabelas, schemas ou dados deste pipeline nessa database
aumentaria o risco de conflito e dificultaria a demonstracao.

## Decisao

Usar uma database PostgreSQL dedicada chamada `open-meteo`.

O projeto passa a usar:

```text
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/open-meteo
DB_NAME=open-meteo
POSTGRES_DB=open-meteo
```

O job `src.jobs.load` tenta criar a database automaticamente quando a
`DATABASE_URL` aponta para PostgreSQL. Como o nome possui hifen, a criacao usa
identificador SQL com aspas.

Tambem foi adicionado suporte as variaveis `DB_HOST`, `DB_PORT`, `DB_NAME`,
`DB_USER` e `DB_PASSWORD`. Quando `DATABASE_URL` nao esta definida, a aplicacao
monta a URL de conexao a partir dessas variaveis.

## Consequencias

Essa decisao isola os dados do projeto Open-Meteo de outras bases locais. A carga
passa a criar ou substituir apenas as tabelas `weather_hourly` e `weather_daily`
dentro da database dedicada.

O uso de hifen no nome da database exige cuidado em comandos SQL manuais. Em
comandos `psql`, quando for necessario referenciar explicitamente o nome em SQL,
use `"open-meteo"`.

No ambiente local do projeto, o `.env` deve ficar ignorado pelo Git e pode conter
as credenciais reais do PostgreSQL da maquina de desenvolvimento.
