@echo off
cd /d "%~dp0"
git pull origin main
call run_aatom.bat
