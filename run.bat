@echo off
REM --- 在這裡設定您的虛擬環境資料夾名稱 ---
set VENV_NAME=venv

REM 自動切換到批次檔所在的目錄
cd /d "%~dp0"

REM 啟用虛擬環境並執行主程式
call "%VENV_NAME%\Scripts\activate.bat"
python main.py

REM 暫停以查看輸出
pause