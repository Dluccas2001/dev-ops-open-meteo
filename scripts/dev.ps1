param(
    [Parameter(Position = 0)]
    [string]$Task = "help"
)

$ErrorActionPreference = "Stop"

function Use-Python {
    if (Test-Path ".venv\Scripts\python.exe") {
        return ".venv\Scripts\python.exe"
    }
    return "python"
}

$Python = Use-Python

switch ($Task) {
    "help" {
        Write-Host "Uso: .\scripts\dev.ps1 <task>"
        Write-Host ""
        Write-Host "Tasks:"
        Write-Host "  setup       cria venv e instala dependencias"
        Write-Host "  lint        executa ruff check"
        Write-Host "  format      formata com ruff"
        Write-Host "  test        executa pytest"
        Write-Host "  run-api     roda FastAPI local"
        Write-Host "  ingest      executa ingestao"
        Write-Host "  transform   executa transformacao"
        Write-Host "  quality     executa checks de qualidade"
        Write-Host "  train       treina modelo"
    }
    "setup" {
        python -m venv .venv
        .venv\Scripts\python -m pip install --upgrade pip
        .venv\Scripts\python -m pip install -r requirements-dev.txt
    }
    "lint" { & $Python -m ruff check . }
    "format" {
        & $Python -m ruff format .
        & $Python -m ruff check . --fix
    }
    "test" { & $Python -m pytest }
    "run-api" { & $Python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000 }
    "ingest" { & $Python -m src.jobs.ingest }
    "transform" { & $Python -m src.jobs.transform }
    "quality" { & $Python -m src.quality.checks }
    "train" { & $Python -m src.ml.train }
    default {
        throw "Task desconhecida: $Task"
    }
}

