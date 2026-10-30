@echo off
cd /d "%~dp0"
echo Creating virtual environment if needed...
if not exist .venv\Scripts\python.exe py -m venv .venv
call .venv\Scripts\activate.bat
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo Launching Streamlit...
python -m streamlit run app.py
pause
