@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 쇼핑 쇼츠 자동 제작기를 켭니다...
python -m shorts web
pause
