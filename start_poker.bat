@echo off
cd /d "C:\Users\evkak\Desktop\pmv-loc\Poker_Mentor_lokal_im"

echo Starting Poker Mentor with full game system...
call poker_venv\Scripts\activate.bat

python -m bot.main

pause