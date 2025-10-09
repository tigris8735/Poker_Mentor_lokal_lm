@echo off
cd /d "C:\Users\evkak\Desktop\www-loc\Poker_Mentor_lokal_im"
echo.

echo ========================================
echo    Poker Mentor Bot Launcher
echo ========================================
echo.

echo Step 1: Checking virtual environment...
if not exist "poker_venv" (
    echo Creating new virtual environment...
    python -m venv poker_venv
)

echo Step 2: Activating virtual environment...
call poker_venv\Scripts\activate.bat

echo Step 3: Installing dependencies...
pip install --upgrade pip
pip install aiogram==3.17.0
pip install aiohttp==3.9.0
pip install sqlalchemy==2.0.23
pip install python-dotenv==1.0.0

echo Step 4: Checking installation...
python -c "import aiogram; import aiohttp; import sqlalchemy; import dotenv; print('✅ All imports successful!')"

echo.
echo Step 5: Starting Poker Mentor Bot...
python -m bot.main

echo.
echo Bot stopped. Press any key to exit...
pause >nul