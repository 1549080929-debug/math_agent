@echo off
chcp 65001 >nul
cd /d "%~dp0"
"C:\Users\殷雅杰\AppData\Local\Programs\Python\Python313\python.exe" main.py %*
pause
