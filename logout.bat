@echo off
echo ============================================
echo   Removendo Credenciais do Windows
echo ============================================

set "TARGET1=LegacyGeneric:target=git:https://github.com"
set "TARGET2=LegacyGeneric:target=gemini:antigravity"

echo Tentando remover: %TARGET1%
cmdkey /delete:"%TARGET1%"

echo.
echo Tentando remover: %TARGET2%
cmdkey /delete:"%TARGET2%"

echo.
echo ============================================
echo   Verificando credenciais restantes...
echo ============================================
cmdkey /list | findstr /i "github gemini:antigravity"
if %errorlevel% neq 0 (
    echo [OK] Nenhuma das credenciais foi encontrada no cofre.
)

echo.
pause