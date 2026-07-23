# ADR 0010 - Fixtures na imagem para bootstrap local no Kind

## Status

Aceita.

## Contexto

O deploy local no Kind usa a imagem `weather-mlops-api:local` sem volumes
persistentes nem acesso direto aos artefatos locais ignorados pelo Git, como
`data/processed`, `models` e `mlruns`.

Com isso, a API sobe corretamente no Kubernetes, mas o endpoint `/model/info`
retorna que o modelo ainda nao esta disponivel ate que o treino seja executado
dentro do ambiente do pod.

## Decisao

Incluir `data/samples` dentro da imagem Docker.

Essa fixture versionada permite executar, dentro do pod:

- transformacao dos dados de amostra;
- data quality;
- treino do modelo;
- geracao de `models/rain_model.joblib`;
- validacao do endpoint `/model/info`.

## Consequencias

Vantagens:

- A demonstracao local no Kind fica reproduzivel.
- O pod consegue gerar o modelo sem depender de volumes externos.
- O CI continua leve, pois `data/samples` e pequeno e versionado.

Trade-offs:

- A imagem passa a carregar uma fixture pequena de dados.
- Em producao real, o ideal seria usar volumes, object storage ou uma etapa de
  pipeline separada para disponibilizar artefatos de modelo.
