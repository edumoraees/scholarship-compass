@echo off
title Limpeza de arquivos grandes do GitHub (git-filter-repo)
color 0a
echo ================================================
echo 🚀 LIMPEZA DE HISTORICO - ARQUIVOS GRANDES
echo ================================================
echo.
echo 🔍 Verificando local atual...
cd /d "%~dp0"
if not exist ".git" (
    echo ❌ ERRO: Nao foi encontrada a pasta .git neste diretorio.
    echo Execute este script dentro da pasta raiz do repositorio.
    pause
    exit /b
)
echo ✅ Repositorio detectado: %cd%
echo.

:: Verifica se o git-filter-repo existe
echo 🔍 Verificando instalacao do git-filter-repo...
where git-filter-repo >nul 2>nul
if %errorlevel%==0 (
    echo ✅ git-filter-repo encontrado!
    set "USE_PYTHON=0"
) else (
    echo ⚠️ git-filter-repo nao encontrado, tentando Python...
    python -m git_filter_repo --version >nul 2>nul
    if %errorlevel%==0 (
        echo ✅ Biblioteca Python git_filter_repo detectada!
        set "USE_PYTHON=1"
    ) else (
        echo ❌ Nenhuma versao do git-filter-repo encontrada.
        echo Instalando via PIP...
        pip install git-filter-repo
        if %errorlevel% neq 0 (
            echo ❌ Falha ao instalar git-filter-repo.
            pause
            exit /b
        )
        set "USE_PYTHON=1"
    )
)

echo.
echo 🚀 Iniciando limpeza do historico de CSVs grandes...
if %USE_PYTHON%==0 (
    git filter-repo --force --path "Sprint 5/Desafio/etapa-1/data/movies.csv" --path "Sprint 5/Desafio/etapa-1/data/series.csv" --invert-paths
) else (
    python -m git_filter_repo --force --path "Sprint 5/Desafio/etapa-1/data/movies.csv" --path "Sprint 5/Desafio/etapa-1/data/series.csv" --invert-paths
)

if %errorlevel% neq 0 (
    echo ❌ Falha ao executar o filtro.
    pause
    exit /b
)

echo.
echo 🧹 Limpando cache e otimizando repositório...
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo.
echo 🔄 Forcando push com historico limpo...
git push origin main --force

echo.
echo ================================================
echo ✅ Processo finalizado!
echo Se o push foi aceito, os arquivos grandes foram removidos.
echo ================================================
pause
