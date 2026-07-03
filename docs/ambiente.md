# Configuracao do ambiente

Este documento registra o ambiente esperado para desenvolver e executar o projeto.

## Ferramentas verificadas nesta maquina

Verificado em 2026-07-02:

- Python: instalado, versao 3.11.9.
- Git: instalado.
- Docker: nao encontrado no PATH.
- Docker Compose: nao encontrado no PATH.
- Make: nao encontrado no PATH.
- kubectl: nao encontrado no PATH.
- Kind: nao encontrado no PATH.
- Trivy: nao encontrado no PATH.

## Ferramentas obrigatorias

- Python 3.11.
- Git.
- Docker Desktop ou Podman.
- Docker Compose ou Podman Compose.
- Make, ou uso alternativo de `scripts/dev.ps1`.
- kubectl.
- Kind.
- Trivy.

## Alternativa enquanto Make nao estiver instalado

No Windows, use:

```powershell
.\scripts\dev.ps1 setup
.\scripts\dev.ps1 lint
.\scripts\dev.ps1 test
.\scripts\dev.ps1 run-api
```

## Instalar dependencias Python

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
```

## Variaveis de ambiente

Crie o `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

## Proximas instalacoes recomendadas no Windows

Com Winget:

```powershell
winget install Docker.DockerDesktop
winget install Kubernetes.kubectl
winget install Kubernetes.kind
winget install AquaSecurity.Trivy
```

Para Make, opcoes comuns:

```powershell
winget install GnuWin32.Make
```

ou instalar Git Bash/Chocolatey/Scoop e disponibilizar `make` no PATH.

