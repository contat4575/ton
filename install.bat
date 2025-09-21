@echo off
echo ========================================
echo ARQV30-AI Data Stage - Instalacao Completa
echo ========================================
echo.

:: Verifica se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado! Por favor, instale Python 3.8+ primeiro.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Verifica se Node.js esta instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Node.js nao encontrado! Por favor, instale Node.js primeiro.
    echo Download: https://nodejs.org/
    pause
    exit /b 1
)

echo [INFO] Python e Node.js detectados com sucesso!
echo.

:: Cria ambiente virtual Python se nao existir
if not exist "venv" (
    echo [SETUP] Criando ambiente virtual Python...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado com sucesso!
) else (
    echo [INFO] Ambiente virtual ja existe.
)

:: Ativa ambiente virtual
echo [SETUP] Ativando ambiente virtual...
call venv\Scripts\activate.bat

:: Instala dependencias Python
echo [SETUP] Instalando dependencias Python...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias Python!
    pause
    exit /b 1
)
echo [OK] Dependencias Python instaladas!

:: Instala dependencias Node.js
echo [SETUP] Instalando dependencias Node.js...
npm install
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias Node.js!
    pause
    exit /b 1
)
echo [OK] Dependencias Node.js instaladas!

:: Cria arquivo .env se nao existir
if not exist ".env" (
    echo [SETUP] Criando arquivo de configuracao .env...
    copy .env.example .env
    echo [AVISO] Configure suas chaves de API no arquivo .env antes de executar!
    echo [AVISO] Edite o arquivo .env e adicione suas chaves:
    echo          - OPENROUTER_API_KEY
    echo          - SERPER_API_KEY
) else (
    echo [INFO] Arquivo .env ja existe.
)

:: Cria diretorio de sessoes
if not exist "sessions" (
    mkdir sessions
    echo [SETUP] Diretorio de sessoes criado.
)

echo.
echo ========================================
echo INSTALACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo PROXIMOS PASSOS:
echo 1. Configure suas chaves de API no arquivo .env
echo 2. Execute run.bat para iniciar o sistema
echo.
echo CHAVES NECESSARIAS:
echo - OPENROUTER_API_KEY: Para acesso aos modelos de IA
echo - SERPER_API_KEY: Para buscas na web
echo.
echo Pressione qualquer tecla para abrir o arquivo .env...
pause >nul
notepad .env