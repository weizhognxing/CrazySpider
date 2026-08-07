@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
".venv\Scripts\python.exe" run.py -c config.yml --serve --serve-host 127.0.0.1 --serve-port 8000
