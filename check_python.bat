@echo off
echo Checking Python installation...
python --version
echo.

echo Checking Python path...
where python
echo.

echo Creating test script...
echo print("Python is working!") > test_python.py
python test_python.py
del test_python.py
echo.

pause