@echo off
cd /d "C:\Users\evkak\Desktop\www-loc\Poker_Mentor_lokal_im"

echo Completely reinstalling Poker Mentor...
echo.

echo Deleting old virtual environment...
if exist "poker_venv" rmdir /s /q poker_venv

echo Creating new virtual environment...
python -m venv poker_venv

echo Activating...
call poker_venv\Scripts\activate.bat

echo Installing packages...
pip install --upgrade pip
pip install aiogram==3.17.0 aiohttp==3.9.0 sqlalchemy==2.0.23 python-dotenv==1.0.0

echo Verification...
python -c "import aiogram; print('aiogram version:', aiogram.__version__)"
python -c "import aiohttp; print('aiohttp version:', aiohttp.__version__)"
python -c "import sqlalchemy; print('SQLAlchemy version:', sqlalchemy.__version__)"

echo.
echo Installation complete! Run start_bot.bat to start the bot.
pause