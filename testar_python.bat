@echo off
REM Script de teste para verificar detecao do Python

echo ========================================
echo TESTE DE DETECAO DO PYTHON
echo ========================================
echo.

echo [1] Testando comando 'python --version':
python --version
if errorlevel 1 (
    echo [ERRO] Python nao foi encontrado!
    echo.
    echo POSSIVEL CAUSA:
    echo - Python nao esta no PATH
    echo - Terminal precisa ser reiniciado apos instalacao
    echo.
) else (
    echo [OK] Python foi detetado com sucesso!
    echo.
)

echo [2] Testando comando 'python -c "import sys; print(sys.version)"':
python -c "import sys; print(sys.version)"
echo.

echo [3] Testando comando 'where python':
where python
echo.

echo [4] Verificando PATH do sistema:
echo %PATH% | findstr /I "python"
if errorlevel 1 (
    echo [AVISO] Nenhum caminho Python encontrado no PATH!
    echo.
    echo SOLUCAO:
    echo 1. Se acabou de instalar Python, FECHE este terminal
    echo 2. Abra um NOVO terminal
    echo 3. Execute novamente este teste
    echo.
) else (
    echo [OK] Python encontrado no PATH do sistema
    echo.
)

echo ========================================
echo FIM DO TESTE
echo ========================================
echo.
pause
