# Plano completo de implementacao - Open-Meteo DevOps/MLOps

Data: 2026-07-02  
Projeto proposto: `weather-mlops-pipeline`  
Fonte de dados: Open-Meteo Weather API  
Objetivo academico: atender aos criterios de avaliacao da disciplina DevOps e MLOps para Engenharia de Dados.

## 1. Objetivo do projeto

Criar um projeto completo de Engenharia de Dados com DevOps e MLOps, usando uma API publica real, pipeline end-to-end, data quality, treinamento de modelo, tracking com MLflow, serving via FastAPI, CI/CD e operacao local em Kubernetes com Kind.

O projeto devera demonstrar:

- Ingestao de dados climaticos da Open-Meteo.
- Persistencia em camada raw.
- Transformacao, limpeza, tipagem e agregacoes
- Validacao de qualidade dos dados.
- Carga em PostgreSQL.
- API de consulta.
- Treinamento de modelo de machine learning.
- Tracking de experimentos com MLflow.
- Serving de predicoes via FastAPI.
- Execucao local via Compose.
- CI com lint, testes, build, scan e validacao de manifests.
- Deploy local em Kind.
- Rollback documentado.
- README, ADRs, diagrama e troubleshooting.

## 2. Fonte de dados escolhida

### Open-Meteo

Site: https://open-meteo.com/  
Documentacao: https://open-meteo.com/en/docs

Motivos da escolha:

- API publica.
- Nao exige API key.
- Retorna JSON limpo.
- Permite dados de previsao e historicos.
- Boa aderencia a pipeline de dados.
- Permite ML simples e explicavel.
- Baixo risco operacional para CI e demos.

### Endpoint inicial

```text
https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&forecast_days=7
```

Variaveis coletadas inicialmente:

- `temperature_2m`
- `relative_humidity_2m`
- `precipitation`
- `wind_speed_10m`

## 3. Escopo funcional

### Cidades iniciais

Usaremos capitais brasileiras para gerar um dataset multi-cidade:

- Sao Paulo
- Rio de Janeiro
- Belo Horizonte
- Curitiba
- Porto Alegre
- Brasilia
- Salvador
- Recife
- Fortaleza
- Manaus

Cada cidade tera:

- nome normalizado;
- latitude;
- longitude;
- estado/UF;
- regiao;
- timezone.

### Pipeline de dados

```text
Open-Meteo API
   |
   v
Job de ingestao
   |
   v
data/raw/open_meteo/{city}/{run_date}.json
   |
   v
Job de transformacao
   |
   v
data/processed/weather_hourly.parquet
data/processed/weather_daily.parquet
   |
   v
Data quality
   |
   v
PostgreSQL
   |
   +----------------+
   |                |
   v                v
FastAPI consulta   Treino ML
                    |
                    v
                  MLflow
                    |
                    v
                Model serving API
```

## 4. Modelo de ML

### Problema inicial

Classificar se vai chover no dia seguinte para uma cidade.

Target:

```text
will_rain_tomorrow = rain_sum_next_day > 0
```

### Features iniciais

- `temp_mean`
- `temp_min`
- `temp_max`
- `humidity_mean`
- `wind_mean`
- `rain_sum`
- `month`
- `day_of_week`
- `city`
- `region`

### Algoritmo inicial

Recomendacao inicial: `RandomForestClassifier`, por lidar bem com nao linearidade e exigir menos engenharia.

Metricas:

- accuracy
- precision
- recall
- f1-score

Artefatos:

- modelo serializado com `joblib`;
- preprocessador, se necessario;
- metricas registradas no MLflow;
- parametros registrados no MLflow;
- exemplo de payload de predicao.

## 5. Stack tecnica

### Linguagem

- Python 3.11

Motivo: melhor compatibilidade com pandas, pyarrow, scikit-learn, MLflow, Pandera e imagens Docker.

### Bibliotecas principais

Runtime:

- `fastapi`
- `uvicorn`
- `requests`
- `pandas`
- `pyarrow`
- `sqlalchemy`
- `psycopg2-binary`
- `pydantic`
- `pydantic-settings`
- `python-dotenv`
- `scikit-learn`
- `mlflow`
- `joblib`
- `pandera`

Desenvolvimento:

- `pytest`
- `httpx`
- `ruff`

### Servicos locais

Via Compose:

- `api`: FastAPI.
- `postgres`: banco relacional para dados processados.
- `mlflow`: tracking de experimentos.

Decisao inicial:

- Usar filesystem local para `raw` e `processed` na primeira entrega.
- Adicionar S3 local apenas se o nucleo estiver estavel.

## 6. Ferramentas necessarias no ambiente

Obrigatorias:

- Git
- Python 3.11
- Make
- Docker ou Podman
- Docker Compose ou Podman Compose
- kubectl
- Kind
- Trivy

Desejaveis:

- GitHub CLI (`gh`)
- kubeconform
- VS Code ou editor equivalente

Verificacao do ambiente:

```bash
git --version
python --version
make --version
docker --version
docker compose version
kubectl version --client
kind version
trivy --version
```

No Windows, se `make` nao estiver disponivel:

- instalar via Chocolatey/Scoop/Git Bash; ou
- usar `mingw32-make`; ou
- criar scripts PowerShell equivalentes.

## 7. Configuracao local Python

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

## 8. Variaveis de ambiente

Arquivo `.env.example`:

```env
ENV=development

APP_NAME=weather-mlops-pipeline
API_HOST=0.0.0.0
API_PORT=8000

OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1/forecast
FORECAST_DAYS=7

DATA_RAW_DIR=data/raw
DATA_PROCESSED_DIR=data/processed
MODEL_DIR=models

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/weather
POSTGRES_DB=weather
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_EXPERIMENT_NAME=weather-rain-prediction
```

## 9. Estrutura de repositorio planejada

```text
.
├── .github/
│   └── workflows/
│       └── ci.yaml
├── config/
│   └── cities.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
├── docs/
│   ├── adr/
│   ├── evidences/
│   ├── architecture.md
│   └── troubleshooting.md
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── ingest-job.yaml
│   └── kustomization.yaml
├── scripts/
├── src/
│   ├── api/
│   │   ├── main.py
│   │   ├── routers/
│   │   └── schemas.py
│   ├── config.py
│   ├── data/
│   │   ├── cities.py
│   │   └── database.py
│   ├── jobs/
│   │   ├── ingest.py
│   │   ├── transform.py
│   │   └── load.py
│   ├── ml/
│   │   ├── features.py
│   │   ├── train.py
│   │   └── predict.py
│   └── quality/
│       └── checks.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── quality/
├── .dockerignore
├── .env.example
├── .gitignore
├── compose.yaml
├── ContainerFile
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## 10. Makefile planejado

Targets essenciais:

```makefile
setup              # instala dependencias locais
lint               # ruff check
format             # ruff format + fix
test               # pytest
quality            # data quality checks
build              # build da imagem
scan               # trivy scan
up                 # sobe compose
down               # derruba compose
logs               # logs compose
ingest             # coleta dados da Open-Meteo
transform          # gera parquet hourly/daily
load               # carrega PostgreSQL
train              # treina modelo e registra MLflow
run-api            # roda FastAPI local
pipeline           # ingest + transform + quality + load + train
validate-k8s       # valida manifests
kind-create        # cria cluster Kind
kind-delete        # remove cluster Kind
deploy             # deploy no Kind
status             # status no Kind
rollback           # rollback local no Kind
clean              # limpa outputs locais
```

## 11. API planejada

Endpoints operacionais:

- `GET /health`
- `GET /metadata`

Endpoints de dados:

- `GET /cities`
- `GET /weather/latest?city=sao-paulo`
- `GET /weather/daily?city=sao-paulo`
- `GET /weather/summary`

Endpoints de ML:

- `GET /model/info`
- `POST /predict/rain`

Payload exemplo:

```json
{
  "city": "sao-paulo",
  "temp_mean": 22.5,
  "temp_min": 18.0,
  "temp_max": 28.0,
  "humidity_mean": 80.0,
  "wind_mean": 12.1,
  "rain_sum": 0.4,
  "month": 7,
  "day_of_week": 3
}
```

Resposta exemplo:

```json
{
  "city": "sao-paulo",
  "will_rain_tomorrow": true,
  "probability": 0.73,
  "model_version": "local"
}
```

## 12. Data quality

Ferramenta escolhida inicialmente:

- Pandera

Motivos:

- Simples de versionar.
- Roda bem no CI.
- Integra naturalmente com pandas.
- Evita infraestrutura extra.

Checks planejados:

- `city` nao nulo.
- `datetime` nao nulo.
- `city + datetime` unico no hourly.
- `date + city` unico no daily.
- temperatura entre `-20` e `55`.
- umidade entre `0` e `100`.
- precipitacao maior ou igual a `0`.
- vento maior ou igual a `0`.
- dataset com numero minimo de linhas.
- colunas obrigatorias presentes.

## 13. Banco de dados

Banco:

- PostgreSQL

Tabelas planejadas:

### `weather_hourly`

- `id`
- `city`
- `uf`
- `region`
- `datetime`
- `temperature_2m`
- `relative_humidity_2m`
- `precipitation`
- `wind_speed_10m`
- `ingested_at`

### `weather_daily`

- `id`
- `city`
- `uf`
- `region`
- `date`
- `temp_min`
- `temp_max`
- `temp_mean`
- `humidity_mean`
- `rain_sum`
- `wind_mean`
- `will_rain`

## 14. Compose planejado

Servicos:

- `api`
- `postgres`
- `mlflow`

Portas:

- API: `8000`
- PostgreSQL: `5432`
- MLflow: `5000`

Volumes:

- `postgres-data`
- `mlflow-data`
- `./data:/app/data`
- `./models:/app/models`

## 15. CI planejado

Arquivo:

```text
.github/workflows/ci.yaml
```

Etapas:

1. Checkout.
2. Setup Python 3.11.
3. Instalar dependencias.
4. Ruff lint.
5. Ruff format check.
6. Pytest.
7. Data quality em fixtures pequenas.
8. Build da imagem.
9. Trivy scan.
10. Validacao de manifests Kubernetes.

Pipeline esperado:

```text
lint -> test -> quality -> build -> scan -> validate
```

## 16. Kubernetes e Kind

Manifests planejados:

- `namespace.yaml`
- `configmap.yaml`
- `secret.yaml`
- `api-deployment.yaml`
- `api-service.yaml`
- `ingest-job.yaml`
- `kustomization.yaml`

Comandos Make:

```bash
make kind-create
make deploy
make status
make rollback
```

Rollback:

```bash
kubectl rollout undo deployment/weather-api -n weather-mlops
```

O README devera explicar:

- como criar o cluster;
- como carregar imagem local no Kind;
- como aplicar manifests;
- como verificar status;
- como simular uma nova versao;
- como executar rollback.

## 17. Documentacao obrigatoria

README devera conter:

- descricao do projeto;
- arquitetura;
- requisitos;
- setup local;
- comandos Make;
- execucao do pipeline;
- acesso a API;
- acesso ao MLflow;
- testes;
- data quality;
- CI;
- deploy Kind;
- rollback;
- troubleshooting;
- decisoes tecnicas.

ADRs planejadas:

1. `0001-open-meteo-como-fonte-de-dados.md`
2. `0002-arquitetura-raw-processed-e-postgres.md`
3. `0003-pandera-para-data-quality.md`
4. `0004-mlflow-para-tracking-e-kind-para-operacao-local.md`

Diagrama em `docs/architecture.md` com Mermaid:

```mermaid
flowchart LR
    A[Open-Meteo API] --> B[Ingest Job]
    B --> C[Raw JSON]
    C --> D[Transform Job]
    D --> E[Processed Parquet]
    E --> F[Data Quality]
    F --> G[PostgreSQL]
    E --> H[Train Model]
    H --> I[MLflow]
    H --> J[Model Artifact]
    G --> K[FastAPI]
    J --> K
```

Troubleshooting em `docs/troubleshooting.md`:

- API Open-Meteo indisponivel.
- Postgres nao subiu.
- MLflow nao acessivel.
- Erro de permissao em volume.
- Porta ocupada.
- Kind nao encontra imagem local.
- Data quality falhou.
- Modelo ainda nao treinado.

## 18. Evidencias

Criar pasta:

```text
docs/evidences/
```

Guardar:

- print ou export de run do MLflow;
- exemplo de chamada ao endpoint `/predict/rain`;
- output de `make quality`;
- output de `make test`;
- evidencia de CI verde;
- evidencia de `make deploy`;
- evidencia de `make rollback`.

## 19. Commits

Usar Conventional Commits:

```text
chore: scaffold project structure
feat: add open-meteo ingestion job
feat: add weather transformation pipeline
test: add unit tests for transform
feat: add pandera data quality checks
feat: add postgres loading job
feat: add ml training with mlflow tracking
feat: add prediction endpoint
ci: add github actions pipeline
docs: add architecture and adr records
```

## 20. Fases de implementacao

### Fase 1 - Scaffold e ambiente

- Criar estrutura base.
- Criar `pyproject.toml`.
- Criar requirements.
- Criar `.env.example`.
- Criar `Makefile`.
- Criar `ContainerFile`.
- Criar `compose.yaml`.
- Criar API minima com `/health`.

Aceite:

- `make setup` funciona.
- `make lint` funciona.
- `make test` funciona.
- `make up` sobe API e Postgres.
- `GET /health` retorna ok.

### Fase 2 - Ingestao

- Criar configuracao de cidades.
- Implementar cliente Open-Meteo.
- Implementar job de ingestao.
- Salvar JSON raw por cidade/data.
- Criar testes com mock de resposta.

Aceite:

- `make ingest` cria arquivos em `data/raw`.
- Testes unitarios passam.

### Fase 3 - Transformacao e qualidade

- Transformar JSON raw em DataFrame hourly.
- Agregar daily.
- Salvar Parquet.
- Criar checks Pandera.
- Criar fixtures pequenas para CI.

Aceite:

- `make transform` gera Parquets.
- `make quality` passa.

### Fase 4 - PostgreSQL e API de consulta

- Criar modelos/tabelas.
- Criar job de carga.
- Criar endpoints `/cities`, `/weather/latest`, `/weather/daily`.
- Criar testes de API.

Aceite:

- `make load` carrega dados.
- Endpoints retornam dados.

### Fase 5 - MLflow e treino

- Criar feature builder.
- Criar script de treino.
- Registrar experimento no MLflow.
- Salvar modelo.
- Criar evidencia.

Aceite:

- `make train` registra run no MLflow.
- Modelo fica disponivel em `models/`.

### Fase 6 - Serving

- Criar endpoint `/predict/rain`.
- Carregar modelo salvo.
- Validar payload com Pydantic.
- Criar teste de predicao.

Aceite:

- `POST /predict/rain` retorna probabilidade e classe.

### Fase 7 - CI

- Criar workflow GitHub Actions.
- Rodar lint, test, quality, build, scan e validate.
- Ajustar fixtures para rodar sem depender de internet.

Aceite:

- CI verde no GitHub.

### Fase 8 - Kubernetes/Kind

- Criar manifests.
- Criar comandos Make para Kind.
- Validar manifests.
- Documentar deploy/status/rollback.

Aceite:

- `make deploy` aplica API no Kind.
- `make status` mostra deployment saudavel.
- `make rollback` executa rollback.

### Fase 9 - Documentacao final

- Completar README.
- Criar ADRs.
- Criar architecture.md.
- Criar troubleshooting.md.
- Adicionar evidencias.

Aceite:

- Projeto pode ser entendido e executado por outra pessoa apenas lendo o README.

## 21. Criterios de aceite final

- [ ] Repositorio organizado.
- [ ] README completo.
- [ ] LICENSE presente.
- [ ] Badges no README.
- [ ] Commits seguindo Conventional Commits.
- [ ] Compose funcional.
- [ ] Pipeline end-to-end funcional.
- [ ] Ingestao Open-Meteo para raw.
- [ ] Transformacao para processed.
- [ ] Data quality configurado.
- [ ] PostgreSQL carregado.
- [ ] API de consulta funcional.
- [ ] Treino ML funcional.
- [ ] MLflow com experimento registrado.
- [ ] Serving de modelo funcional.
- [ ] Testes automatizados.
- [ ] CI com lint, test, build, scan e validate.
- [ ] Manifests Kubernetes.
- [ ] Deploy no Kind via Makefile.
- [ ] Status e rollback via Makefile.
- [ ] Pelo menos 3 ADRs.
- [ ] Diagrama de arquitetura.
- [ ] Troubleshooting.
- [ ] Evidencias de MLflow e operacao.

## 22. Estrategia de execucao

A prioridade e entregar o nucleo funcionando antes de sofisticar:

1. Pipeline local completo.
2. Testes e data quality.
3. API e ML.
4. CI."
5. Kind e rollback.
6. Documentacao e evidencias.
7. Bonus apenas se houver tempo.

O projeto sera construido para ser demonstravel com poucos comandos:

```bash
make up
make pipeline
make test
make quality
make train
make deploy
make status
make rollback
```

## 23. Decisao inicial importante

Nao usaremos o dataset completo de CNPJ nesta implementacao inicial.

Motivo:

- O volume e alto.
- A integracao e mais arriscada.
- O foco da avaliacao e projeto completo, CI, operacao e MLOps.
- Open-Meteo reduz risco e permite demonstrar todos os criterios com clareza.
