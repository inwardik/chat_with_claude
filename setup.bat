@echo off
chcp 65001 >nul
echo ====================================
echo Установка системы поиска по документам
echo ====================================
echo.

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.8 или выше.
    pause
    exit /b 1
)

echo ✓ Python найден
echo.

REM Создание виртуального окружения (опционально)
echo Создать виртуальное окружение? (рекомендуется)
set /p CREATE_VENV="Введите Y для создания или N для пропуска: "

if /i "%CREATE_VENV%"=="Y" (
    echo Создаем виртуальное окружение...
    python -m venv venv
    echo ✓ Виртуальное окружение создано
    echo.
    echo Активируем окружение...
    call venv\Scripts\activate.bat
)

REM Установка зависимостей
echo Устанавливаем зависимости...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)

echo.
echo ✓ Зависимости установлены
echo.

REM Создание .env если не существует
if not exist .env (
    echo Создаем файл .env...
    copy .env.example .env >nul
    echo ✓ Файл .env создан
    echo.
)

REM Создание папки documents если не существует
if not exist documents (
    echo Создаем папку documents...
    mkdir documents
    echo ✓ Папка documents создана
    echo.
)

echo ====================================
echo ✓ Установка завершена!
echo ====================================
echo.
echo Следующие шаги:
echo.
echo 1. Поместите ваши документы (.txt, .md) в папку "documents"
echo.
echo 2. Запустите индексацию:
echo    python indexer.py
echo.
echo 3. Откройте проект в Claude Code
echo    - MCP сервер настроен через .mcp.json
echo    - Одобрите использование MCP сервера при первом запуске
echo    - Готово! Никаких дополнительных настроек не требуется
echo.
echo Подробнее см. QUICKSTART.md или MCP_SETUP.md
echo.
pause
