@echo off
REM ============================================================================
REM  DGT Rasters - Launcher Script
REM  Projeto criado com apoio de GitHub Copilot AI
REM ============================================================================

echo.
echo ========================================================================
echo   DGT RASTERS - Sistema de Download de Dados Geoespaciais
echo ========================================================================
echo.

REM Ir para o diretório do script
cd /d "%~dp0"

REM Verificar se o virtual environment existe
if not exist "dgt_venv\" (
    echo [SETUP] Virtual environment nao encontrado. A criar...
    echo.
    python -m venv dgt_venv
    
    if errorlevel 1 (
        echo [ERRO] Falha ao criar virtual environment
        echo Por favor, certifique-se de que Python 3.8+ esta instalado
        pause
        exit /b 1
    )
    
    echo [OK] Virtual environment criado: dgt_venv
    echo.
)

REM Ativar o virtual environment
echo [SETUP] A ativar ambiente virtual...
call dgt_venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERRO] Falha ao ativar virtual environment
    pause
    exit /b 1
)

echo [OK] Ambiente virtual ativado
echo.

REM Instalar/atualizar dependências
echo [SETUP] A verificar dependencias...
pip install --upgrade pip -q
pip install -r requirements.txt -q

if errorlevel 1 (
    echo [AVISO] Algumas dependencias podem nao ter sido instaladas
    echo.
)

echo [OK] Dependencias verificadas
echo.

REM Verificar se caminhos.json existe
if not exist "config\caminhos.json" (
    echo [AVISO] Ficheiro config\caminhos.json nao encontrado!
    echo Por favor, copie config\caminhos.json.template para config\caminhos.json
    echo e configure suas credenciais.
    echo.
    pause
    exit /b 1
)

REM Iniciar a aplicação
echo ========================================================================
echo   A iniciar interface grafica...
echo ========================================================================
echo.

python src\seletor_projeto.py

if errorlevel 1 (
    echo.
    echo [ERRO] A aplicacao terminou com erro
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo   Aplicacao encerrada
echo ========================================================================
echo.
pause