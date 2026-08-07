@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PLAYWRIGHT_CHROMIUM_EXECUTABLE=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
cd /d "%~dp0"
".venv\Scripts\python.exe" -m tools.cookie_fetcher --config config.yml --output config\cookies.json
