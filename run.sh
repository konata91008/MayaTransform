#!/bin/bash
# -----------------------------------------------------------------
# -- macOS/Linux 啟動腳本 for MayaTransform
# -- 功能：
# -- 1. 檢查 Python3 是否安裝。
# -- 2. 建立一個名為 venv 的虛擬環境 (如果尚未建立)。
# -- 3. 啟用虛擬環境。
# -- 4. 根據 requirements.txt 安裝所有必要的套件。
# -- 5. 執行主程式 main.py。
# -----------------------------------------------------------------

echo ""
echo "[1/4] 正在檢查 Python 環境..."

# 檢查系統是否安裝了 python3
if ! command -v python3 &> /dev/null
then
    echo ""
    echo "[錯誤] 系統中找不到 Python3。"
    echo "請先安裝 Python 3.8 或以上版本。"
    exit 1
fi

echo "Python3 已安裝。"

# 檢查 venv 資料夾是否存在
if [ ! -d "venv" ]; then
    echo ""
    echo "[2/4] 偵測到首次執行，正在建立虛擬環境 (venv)..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo ""
        echo "[錯誤] 建立虛擬環境失敗。"
        exit 1
    fi
    echo "虛擬環境建立成功。"
else
    echo ""
    echo "[2/4] 虛擬環境已存在，跳過建立步驟。"
fi

echo ""
echo "[3/4] 正在啟用虛擬環境並安裝所需套件..."

# 啟用虛擬環境並安裝套件
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "[錯誤] 從 requirements.txt 安裝套件失敗。"
    exit 1
fi

echo "套件安裝完成。"

echo ""
echo "[4/4] 正在啟動 MayaTransform 應用程式..."
echo ""

# 執行主程式
python3 main.py

echo ""
echo "應用程式已關閉。"
