@echo off
REM ============================================================================
REM  DGT Rasters - Launcher Script
REM  Projeto criado com apoio de GitHub Copilot AI
REM ============================================================================

REM Configurar codepage UTF-8 para suportar caracteres Unicode
chcp 65001 >nul 2>&1

echo.
echo ========================================================================
echo   DGT RASTERS - Sistema de Download de Dados Geoespaciais
echo ========================================================================
echo.

REM Ir para o diretório do script
cd /d "%~dp0"

REM Verificar se é primeira execução (venv não existe)
set "FIRST_RUN=0"
if not exist "dgt_venv\" (
    set "FIRST_RUN=1"
    
    echo [PRIMEIRA EXECUCAO] Detectada!
    echo [INFO] Iniciando assistente de configuracao...
    echo.
    
    REM Mostrar janela de boas-vindas
    powershell -ExecutionPolicy Bypass -File "config\setup_inicial.ps1" Show-WelcomeDialog
    if errorlevel 1 (
        echo [INFO] Configuracao cancelada pelo utilizador.
        pause
        exit /b 0
    )
    
    echo [SETUP] A criar virtual environment...
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

REM Verificar se o Python do venv existe
if not exist "dgt_venv\Scripts\python.exe" (
    echo [ERRO] Virtual environment nao foi criado corretamente
    echo Por favor, verifique se Python 3.8+ esta instalado
    pause
    exit /b 1
)

echo [OK] Ambiente virtual encontrado
echo.

REM Instalar/atualizar dependências usando o Python do venv
echo [SETUP] A verificar dependencias...
echo.
dgt_venv\Scripts\python.exe -m pip install --upgrade pip
echo.
dgt_venv\Scripts\python.exe -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar algumas dependencias!
    echo Por favor, verifique os erros acima e tente novamente.
    echo.
    pause
    exit /b 1
)

echo [OK] Dependencias verificadas
echo.

REM Verificar se caminhos.json existe
if not exist "config\caminhos.json" (
    if "%FIRST_RUN%"=="1" (
        echo [CONFIGURACAO] Ficheiro config\caminhos.json nao encontrado
        echo [INFO] Solicitando credenciais DGT...
        echo.
        
        REM Copiar template se existir
        if exist "config\caminhos.json.template" (
            copy "config\caminhos.json.template" "config\caminhos.json" >nul
        )
        
        REM Solicitar credenciais via PowerShell
        powershell -ExecutionPolicy Bypass -Command "& { $scriptPath = Join-Path '%~dp0' 'config\setup_inicial.ps1'; . $scriptPath; $creds = Show-CredentialsDialog; if ($creds) { $configPath = Join-Path '%~dp0' 'config\caminhos.json'; if (Test-Path $configPath) { $config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json; $config.credentials.username = $creds.Username; $config.credentials.password = $creds.Password; $json = $config | ConvertTo-Json -Depth 10; [System.IO.File]::WriteAllText($configPath, $json, [System.Text.UTF8Encoding]::new($false)); exit 0 } else { exit 2 } } else { exit 1 } }"
        
        if errorlevel 2 (
            echo [ERRO] Ficheiro de configuracao nao encontrado
            pause
            exit /b 1
        )
        
        if errorlevel 1 (
            echo [INFO] Configuracao cancelada pelo utilizador
            pause
            exit /b 0
        )
        
        echo [OK] Credenciais configuradas com sucesso
        echo.
    ) else (
        echo [AVISO] Ficheiro config\caminhos.json nao encontrado!
        echo Por favor, copie config\caminhos.json.template para config\caminhos.json
        echo e configure suas credenciais.
        echo.
        pause
        exit /b 1
    )
)

REM Iniciar a aplicação
echo ========================================================================
echo   A iniciar interface grafica...
echo ========================================================================
echo.

dgt_venv\Scripts\python.exe src\seletor_projeto.py

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