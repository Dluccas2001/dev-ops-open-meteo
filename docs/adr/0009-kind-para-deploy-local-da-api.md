# ADR 0009 - Kind para deploy local da API

## Status

Aceita

## Contexto

O projeto precisa demonstrar operacao local em Kubernetes, incluindo deploy,
status e rollback. A solucao deve rodar em ambiente de desenvolvimento sem cloud
e com baixo custo operacional.

## Decisao

Usar Kind para criar um cluster Kubernetes local e aplicar manifests em `k8s/`.

Os manifests criados incluem:

- namespace `weather-mlops`;
- ConfigMap para configuracoes nao sensiveis;
- Secret com valores exemplo para credenciais;
- Deployment da FastAPI;
- Service ClusterIP para acesso via `kubectl port-forward`;
- Job Kubernetes para executar a ingestao.

A imagem `weather-mlops-api:local` deve ser construida com Docker e carregada no
cluster Kind com `kind load docker-image`.

## Consequencias

Essa decisao atende ao criterio de operacao local da disciplina sem depender de
provedor cloud. O Service como ClusterIP evita expor portas diretamente e torna o
acesso explicito via port-forward.

Credenciais reais nao devem ser versionadas. O arquivo `k8s/secret.yaml` contem
valores de exemplo para demonstracao e deve ser ajustado localmente quando a API
precisar acessar PostgreSQL fora do cluster.
