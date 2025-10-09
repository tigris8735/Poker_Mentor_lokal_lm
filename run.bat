@echo off
cd /d "C:\Users\evkak\Desktop\www-loc\Poker_Mentor_lokal_im"

echo Checking environment...
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env file with your tokens!
    pause
    exit
)

if exist "poker_venv\Scripts\activate" (
    call poker_venv\Scripts\activate
) else (
    echo Creating virtual environment...
    python -m venv poker_venv
    call poker_venv\Scripts\activate
    pip install aiogram==3.17.0 aiohttp==3.9.0 sqlalchemy==2.0.23 python-dotenv==1.0.0
)

echo Running system check...
python full_check.py

echo.
echo Starting Poker Mentor Bot...
python -m bot.main
pause