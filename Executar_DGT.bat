@echo off@echo off

REM ============================================================================REM ============================================================================

REM  DGT Rasters - Launcher ScriptREM  DGT Rasters - Launcher Script

REM  Projeto criado com apoio de GitHub Copilot AIREM  Projeto criado com apoio de GitHub Copilot AI

REM ============================================================================REM ============================================================================



REM Configurar codepage UTF-8 para suportar caracteres UnicodeREM Configurar codepage UTF-8 para suportar caracteres Unicode

chcp 65001 >nul 2>&1chcp 65001 >nul 2>&1



echo.echo.

echo ========================================================================echo ========================================================================

echo   DGT RASTERS - Sistema de Download de Dados Geoespaciaisecho   DGT RASTERS - Sistema de Download de Dados Geoespaciais

echo ========================================================================echo ========================================================================

echo.echo.



REM Ir para o diretorio do scriptREM Ir para o diretorio do script

cd /d "%~dp0"cd /d "%~dp0"



REM Verificar se e primeira execucao (venv nao existe)REM Verificar se e primeira execucao (venv nao existe)

set "FIRST_RUN=0"set "FIRST_RUN=0"

if not exist "dgt_venv\" (if not exist "dgt_venv\" (

    set "FIRST_RUN=1"    set "FIRST_RUN=1"

        

    echo [PRIMEIRA EXECUCAO] Detectada!    echo [PRIMEIRA EXECUCAO] Detectada!

    echo [INFO] Iniciando assistente de configuracao...    echo [INFO] Iniciando assistente de configuracao...

    echo.    echo.

        

    REM Mostrar janela de boas-vindas    REM Mostrar janela de boas-vindas

    powershell -ExecutionPolicy Bypass -File "config\setup_inicial.ps1" Show-WelcomeDialog    powershell -ExecutionPolicy Bypass -File "config\setup_inicial.ps1" Show-WelcomeDialog

    if errorlevel 1 (    if errorlevel 1 (

        echo [INFO] Configuracao cancelada pelo utilizador.        echo [INFO] Configuracao cancelada pelo utilizador.

        pause        pause

        exit /b 0        exit /b 0

    )    )

        

    echo [SETUP] A criar virtual environment...    echo [SETUP] A criar virtual environment...

    echo.    echo.

    python -m venv dgt_venv    python -m venv dgt_venv

        

    if errorlevel 1 (    if errorlevel 1 (

        echo [ERRO] Falha ao criar virtual environment        echo [ERRO] Falha ao criar virtual environment

        echo Por favor, certifique-se de que Python 3.8+ esta instalado        echo Por favor, certifique-se de que Python 3.8+ esta instalado

        pause        pause

        exit /b 1        exit /b 1

    )    )

        

    echo [OK] Virtual environment criado: dgt_venv    echo [OK] Virtual environment criado: dgt_venv

    echo.    echo.

))



REM Verificar se o Python do venv existeREM Verificar se o Python do venv existe

if not exist "dgt_venv\Scripts\python.exe" (if not exist "dgt_venv\Scripts\python.exe" (

    echo [ERRO] Virtual environment nao foi criado corretamente    echo [ERRO] Virtual environment nao foi criado corretamente

    echo Por favor, verifique se Python 3.8+ esta instalado    echo Por favor, verifique se Python 3.8+ esta instalado

    pause    pause

    exit /b 1    exit /b 1

))



echo [OK] Ambiente virtual encontradoecho [OK] Ambiente virtual encontrado

echo.echo.



REM Instalar/atualizar dependencias usando o Python do venvREM Instalar/atualizar dependencias usando o Python do venv

echo [SETUP] A verificar dependencias...echo [SETUP] A verificar dependencias...

echo.echo.

dgt_venv\Scripts\python.exe -m pip install --upgrade pipdgt_venv\Scripts\python.exe -m pip install --upgrade pip

echo.echo.

dgt_venv\Scripts\python.exe -m pip install -r requirements.txtdgt_venv\Scripts\python.exe -m pip install -r requirements.txt



if errorlevel 1 (if errorlevel 1 (

    echo.    echo.

    echo [ERRO] Falha ao instalar algumas dependencias!    echo [ERRO] Falha ao instalar algumas dependencias!

    echo Por favor, verifique os erros acima e tente novamente.    echo Por favor, verifique os erros acima e tente novamente.

    echo.    echo.

    pause    pause

    exit /b 1    exit /b 1

))



echo [OK] Dependencias verificadasecho [OK] Dependencias verificadas

echo.echo.



REM Verificar se caminhos.json existeREM Verificar se caminhos.json existe

if not exist "config\caminhos.json" (if not exist "config\caminhos.json" (

    if "%FIRST_RUN%"=="1" (    if "%FIRST_RUN%"=="1" (

        echo [CONFIGURACAO] Ficheiro config\caminhos.json nao encontrado        echo [CONFIGURACAO] Ficheiro config\caminhos.json nao encontrado

        echo [INFO] Solicitando credenciais DGT...        echo [INFO] Solicitando credenciais DGT...

        echo.        echo.

                

        REM Copiar template se existir        REM Copiar template se existir

        if exist "config\caminhos.json.template" (        if exist "config\caminhos.json.template" (

            copy "config\caminhos.json.template" "config\caminhos.json" >nul            copy "config\caminhos.json.template" "config\caminhos.json" >nul

        )        )

                

        REM Solicitar credenciais via PowerShell        REM Solicitar credenciais via PowerShell

        powershell -ExecutionPolicy Bypass -Command "& { $scriptPath = Join-Path '%~dp0' 'config\setup_inicial.ps1'; . $scriptPath; $creds = Show-CredentialsDialog; if ($creds) { $configPath = Join-Path '%~dp0' 'config\caminhos.json'; if (Test-Path $configPath) { $config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json; $config.credentials.username = $creds.Username; $config.credentials.password = $creds.Password; $json = $config | ConvertTo-Json -Depth 10; [System.IO.File]::WriteAllText($configPath, $json, [System.Text.UTF8Encoding]::new($false)); exit 0 } else { exit 2 } } else { exit 1 } }"        powershell -ExecutionPolicy Bypass -Command "& { $scriptPath = Join-Path '%~dp0' 'config\setup_inicial.ps1'; . $scriptPath; $creds = Show-CredentialsDialog; if ($creds) { $configPath = Join-Path '%~dp0' 'config\caminhos.json'; if (Test-Path $configPath) { $config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json; $config.credentials.username = $creds.Username; $config.credentials.password = $creds.Password; $json = $config | ConvertTo-Json -Depth 10; [System.IO.File]::WriteAllText($configPath, $json, [System.Text.UTF8Encoding]::new($false)); exit 0 } else { exit 2 } } else { exit 1 } }"

                

        if errorlevel 2 (        if errorlevel 2 (

            echo [ERRO] Ficheiro de configuracao nao encontrado            echo [ERRO] Ficheiro de configuracao nao encontrado

            pause            pause

            exit /b 1            exit /b 1

        )        )

                

        if errorlevel 1 (        if errorlevel 1 (

            echo [INFO] Configuracao cancelada pelo utilizador            echo [INFO] Configuracao cancelada pelo utilizador

            pause            pause

            exit /b 0            exit /b 0

        )        )

                

        echo [OK] Credenciais configuradas com sucesso        echo [OK] Credenciais configuradas com sucesso

        echo.        echo.

    ) else (    ) else (

        echo [AVISO] Ficheiro config\caminhos.json nao encontrado!        echo [AVISO] Ficheiro config\caminhos.json nao encontrado!

        echo Por favor, copie config\caminhos.json.template para config\caminhos.json        echo Por favor, copie config\caminhos.json.template para config\caminhos.json

        echo e configure suas credenciais.        echo e configure suas credenciais.

        echo.        echo.

        pause        pause

        exit /b 1        exit /b 1

    )    )

))



REM Iniciar a aplicacaoREM Iniciar a aplicacao

echo ========================================================================echo ========================================================================

echo   A iniciar interface grafica...echo   A iniciar interface grafica...

echo ========================================================================echo ========================================================================

echo.echo.



dgt_venv\Scripts\python.exe src\seletor_projeto.pydgt_venv\Scripts\python.exe src\seletor_projeto.py



if errorlevel 1 (if errorlevel 1 (

    echo.    echo.

    echo [ERRO] A aplicacao terminou com erro    echo [ERRO] A aplicacao terminou com erro

    pause    pause

    exit /b 1    exit /b 1

))



echo.echo.

echo ========================================================================echo ========================================================================

echo   Aplicacao encerradaecho   Aplicacao encerrada

echo ========================================================================echo ========================================================================

echo.echo.

pausepause
