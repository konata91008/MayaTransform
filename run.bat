@echo off
REM -----------------------------------------------------------------
REM -- Windows 啟動腳本 for MayaTransform
REM -- 功能：
REM -- 1. 檢查 Python 是否安裝。
REM -- 2. 建立一個名為 venv 的虛擬環境 (如果尚未建立)。
REM -- 3. 啟用虛擬環境。
REM -- 4. 根據 requirements.txt 安裝所有必要的套件。
REM -- 5. 執行主程式 main.py。
REM -----------------------------------------------------------------

echo.
echo [1/4] 正在檢查 Python 環境...

REM 檢查系統是否安裝了 python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [錯誤] 系統中找不到 Python。
    echo 請先安裝 Python 3.8 或以上版本，並將其加入到系統 PATH 環境變數中。
    pause
    exit /b
)

echo Python 已安裝。

REM 檢查 venv 資料夾是否存在
if not exist "venv" (
    echo.
    echo [2/4] 偵測到首次執行，正在建立虛擬環境 (venv)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo.
        echo [錯誤] 建立虛擬環境失敗。
        pause
        exit /b
    )
    echo 虛擬環境建立成功。
) else (
    echo.
    echo [2/4] 虛擬環境已存在，跳過建立步驟。
)


echo.
echo [3/4] 正在啟用虛擬環境並安裝所需套件...

REM 啟用虛擬環境並安裝套件
call "venv\Scripts\activate.bat"
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [錯誤] 從 requirements.txt 安裝套件失敗。
    pause
    exit /b
)

echo 套件安裝完成。

echo.
echo [4/4] 正在啟動 MayaTransform 應用程式...
echo.

REM 執行主程式
python main.py

echo.
echo 應用程式已關閉。
pause
