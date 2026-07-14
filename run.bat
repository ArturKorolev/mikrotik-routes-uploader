@echo off
REM Быстрый запуск MikroTik Routes Uploader на Windows

echo =============================================
echo MikroTik Routes Uploader
echo =============================================

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python не найден!
    echo Пожалуйста, установите Python с https://www.python.org/
    echo Убедитесь, что отметили "Add Python to PATH"
    pause
    exit /b 1
)

REM Проверка зависимостей
echo.
echo Проверка зависимостей...
pip list | findstr "routeros-api" >nul
if errorlevel 1 (
    echo Установка routeros-api...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Не удалось установить зависимости!
        pause
        exit /b 1
    )
)

REM Запуск приложения
echo.
echo Запуск приложения...
python upload_route_gui.py

REM Если ошибка
if errorlevel 1 (
    echo.
    echo ERROR: Приложение завершилось с ошибкой!
    pause
    exit /b 1
)

pause
