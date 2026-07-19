# ADR 0003 - Pandera para data quality

## Status

Aceita

## Contexto

O pipeline precisa validar que os dados transformados possuem colunas obrigatorias,
tipos esperados, intervalos plausiveis e unicidade nas chaves de tempo e cidade.

A solucao deve ser simples de executar em ambiente local e no GitHub Actions, sem
exigir infraestrutura adicional.

## Decisao

Usar Pandera para implementar os checks de qualidade dos datasets processados.

Checks planejados:

- campos `city`, `datetime` e `date` nao nulos;
- unicidade de `city + datetime` no dataset horario;
- unicidade de `city + date` no dataset diario;
- temperatura entre `-20` e `55`;
- umidade entre `0` e `100`;
- precipitacao maior ou igual a `0`;
- velocidade do vento maior ou igual a `0`;
- quantidade minima de linhas;
- colunas obrigatorias presentes.

## Consequencias

Pandera integra naturalmente com pandas, e os checks podem rodar tanto no
desenvolvimento local quanto no CI. Isso torna as falhas de qualidade explicitas
antes da carga no PostgreSQL e antes do treinamento do modelo.

A decisao tambem evita a necessidade de ferramentas mais pesadas de observabilidade
de dados nesta fase inicial.
