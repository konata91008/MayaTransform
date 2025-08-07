import customtkinter as ctk
import tkinterdnd2 as TkinterDnD
from app import MayaTransformApp

if __name__ == "__main__":
    """
    程式主進入點。
    先初始化一個支援 TkinterDnD 的主視窗，然後在其上建立 CustomTkinter 應用。
    """
    # 建立支援拖放功能的根視窗
    root = TkinterDnD.Tk()
    
    # --- 關鍵設定：明確設定外觀模式為 "light" (淺色) ---
    ctk.set_appearance_mode("light") 
    
    # 設定預設顏色主題
    ctk.set_default_color_theme("blue")

    # --- 新增的修復程式碼 ---
    # 手動將根視窗的背景色設定為淺色主題的顏色
    root.configure(bg="#F9F9FA")

    # 傳遞根視窗來建立應用程式
    app = MayaTransformApp(root)
    root.mainloop()
