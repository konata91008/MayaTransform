# MayaTransform
一個使用 Python 和 CustomTkinter 製作的桌面應用程式，專門用於 EPUB 電子書和 SRT/ASS 字幕的簡繁體中文轉換。

## 功能特色
-   支援 EPUB 和 SRT/ASS 檔案格式。
-   提供「簡轉繁」與「繁轉簡」兩種轉換模式。
-   支援批次處理多個檔案。
-   提供檔案拖放功能，操作直觀。
-   支援多國語言介面 (繁中、英文、日文)。

## 如何使用
1.  下載整個專案。
2.  (Windows) 直接雙擊 `run.bat`。
3.  (macOS/Linux) 先在終端機執行 `chmod +x run.sh` 給予權限，然後執行 `./run.sh`。
4.  腳本會自動建立虛擬環境並安裝所有必要的套件。
5.  享受使用！

## 使用的套件

-   CustomTkinter
-   opencc-python-reimplemented
-   ebooklib
-   beautifulsoup4
-   tkinterdnd2-universal