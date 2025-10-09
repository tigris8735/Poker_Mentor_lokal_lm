@echo off
cd /d "C:\Users\evkak\Desktop\www-loc\Poker_Mentor_lokal_im"
if exist "poker_venv\Scripts\activate" (
    call poker_venv\Scripts\activate
    echo Virtual environment activated
) else (
    echo Creating virtual environment...
    python -m venv poker_venv
    call poker_venv\Scripts\activate
    pip install aiogram==3.17.0 aiohttp==3.9.0 sqlalchemy==2.0.23 python-dotenv==1.0.0
)

echo Starting Poker Mentor Bot...
python -m bot.main
pause