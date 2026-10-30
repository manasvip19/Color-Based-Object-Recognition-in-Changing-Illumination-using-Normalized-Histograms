@echo off
cd /d "%~dp0"
echo Starting Color-Based Object Recognition Streamlit app...
py -m streamlit run app.py
if errorlevel 1 (
  echo.
  echo If dependencies are missing, run: py -m pip install -r requirements.txt
  pause
)
