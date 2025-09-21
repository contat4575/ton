@echo off
echo ========================================
echo ARQV30-AI Data Stage - Iniciando Sistema
echo ========================================
echo.

:: Verifica se o ambiente virtual existe
if not exist "venv" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute install.bat primeiro para configurar o sistema.
    pause
    exit /b 1
)

:: Verifica se node_modules existe
if not exist "node_modules" (
    echo [ERRO] Dependencias Node.js nao encontradas!
    echo Execute install.bat primeiro para configurar o sistema.
    pause
    exit /b 1
)

:: Verifica se arquivo .env existe
if not exist ".env" (
    echo [AVISO] Arquivo .env nao encontrado!
    echo Copiando .env.example para .env...
    copy .env.example .env
    echo [AVISO] Configure suas chaves de API no arquivo .env!
    notepad .env
    echo Pressione qualquer tecla apos configurar as chaves...
    pause >nul
)

echo [INFO] Iniciando ARQV30-AI Data Stage...
echo.

:: Ativa ambiente virtual
call venv\Scripts\activate.bat

:: Inicia o backend FastAPI em background
echo [BACKEND] Iniciando servidor FastAPI na porta 8000...
start python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

:: Aguarda alguns segundos para o backend inicializar
echo [INFO] Aguardando inicializacao do backend...
timeout /t 5 /nobreak >nul

:: Verifica se o backend esta rodando
echo [INFO] Verificando se o backend esta ativo...
curl -s http://localhost:8000/docs >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Backend pode estar ainda inicializando...
    echo Aguardando mais alguns segundos...
    timeout /t 5 /nobreak >nul
)

:: Inicia o frontend React em background
echo [FRONTEND] Iniciando servidor de desenvolvimento React...
start /B npm run dev

:: Aguarda o frontend inicializar
echo [INFO] Aguardando inicializacao do frontend...
timeout /t 8 /nobreak >nul

:: Abre o navegador
echo [INFO] Abrindo navegador...
start http://localhost:5173

echo.
echo ========================================
echo SISTEMA INICIADO COM SUCESSO!
echo ========================================
echo.
echo SERVICOS ATIVOS:
echo - Backend API: http://localhost:8000
echo - Frontend Web: http://localhost:5173
echo - Documentacao API: http://localhost:8000/docs
echo.
echo COMANDOS UTEIS:
echo - Para parar os servicos: Ctrl+C em cada janela
echo - Para reiniciar: Execute run.bat novamente
echo - Para reconfigurar: Execute install.bat
echo.
echo [INFO] O navegador deve abrir automaticamente.
echo [INFO] Se nao abrir, acesse: http://localhost:5173
echo.
echo Pressione qualquer tecla para ver os logs do sistema...
pause >nul

:: Mostra logs em tempo real (opcional)
echo.
echo ========================================
echo LOGS DO SISTEMA (Ctrl+C para sair)
echo ========================================
echo.
echo [INFO] Monitorando logs do backend...
echo [INFO] Para ver logs detalhados, verifique as janelas abertas.
echo.

:: Mantem o script rodando para mostrar status
:loop
timeout /t 30 /nobreak >nul
echo [%date% %time%] Sistema rodando... (Ctrl+C para parar)
goto loop