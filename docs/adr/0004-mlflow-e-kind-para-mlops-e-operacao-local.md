# ADR 0004 - MLflow e Kind para MLOps e operacao local

## Status

Aceita

## Contexto

O projeto precisa demonstrar integracao MLOps e praticas DevOps alem do pipeline
de dados. Isso inclui tracking de experimentos, artefatos de modelo, serving via
API, conteinerizacao e operacao local com possibilidade de rollback.

A solucao deve funcionar em uma maquina de desenvolvimento, usando ferramentas
comuns em projetos de dados e engenharia de software.

## Decisao

Usar MLflow para tracking de experimentos e registro de metricas, parametros e
artefatos do modelo.

Usar Docker Compose para operacao local dos servicos principais:

- API FastAPI;
- PostgreSQL;
- MLflow.

Usar Kubernetes local com Kind para demonstrar deploy, status e rollback da API.

## Consequencias

MLflow permite evidenciar o ciclo de treinamento, comparacao de metricas e
persistencia do modelo gerado. Compose facilita a execucao integrada durante o
desenvolvimento e a demonstracao.

Kind permite exercitar conceitos de operacao em Kubernetes sem depender de cloud.
A contrapartida e que Docker, kubectl, Kind e Trivy passam a ser dependencias
necessarias para as fases finais do projeto.
