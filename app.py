import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# 從 utils 模組匯入
from utils.translations import get_translations

# 從 ui 模組匯入 (現在使用 customtkinter)
from ui.epub_tab import EpubTab
from ui.subtitle_tab import SubtitleTab
from ui.common_widgets import create_header, create_common_controls

# 從 logic 模組匯入
from logic.epub_converter import run_epub_conversion
from logic.subtitle_converter import run_subtitle_conversion

class MayaTransformApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MayaTransform v1.1")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        self.root.minsize(700, 600)

        # --- 初始化設定 ---
        self.translations = get_translations()
        self.current_lang = "zh_TW"
        self._ = lambda s: self.translations[self.current_lang].get(s, s)
        
        # --- 核心資料與變數 ---
        self.epub_file_queue = []
        self.epub_file_count_text = tk.StringVar()
        self.epub_conversion_direction = tk.StringVar()
        
        self.subtitle_file_queue = []
        self.subtitle_file_count_text = tk.StringVar()
        self.subtitle_conversion_direction = tk.StringVar()

        self.output_dir = tk.StringVar()
        self.status_text = tk.StringVar()
        
        self.create_widgets()
        self.update_language()

    def create_widgets(self):
        # 設定主框架的 Grid 佈局
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # 建立頂部標題和語言切換按鈕 (放置在 root 中)
        self.header_frame = create_header(self.root, self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # 建立分頁系統
        self.tab_view = ctk.CTkTabview(self.root, corner_radius=8)
        self.tab_view.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        
        # 建立並加入分頁 (使用固定的、非翻譯的內部名稱作為 key)
        self.tab_view.add("epub")
        self.tab_view.add("subtitle")
        
        # --- 設定分頁背景色以防止閃爍 (已修正) ---
        # 使用正確的方式從主題中取得淺色模式的背景顏色 (索引 [0])
        light_bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0]
        self.tab_view.tab("epub").configure(fg_color=light_bg_color)
        self.tab_view.tab("subtitle").configure(fg_color=light_bg_color)

        # 將分頁內容放入對應的 Tab 中
        self.epub_tab_frame = EpubTab(self.tab_view.tab("epub"), self)
        self.epub_tab_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.subtitle_tab_frame = SubtitleTab(self.tab_view.tab("subtitle"), self)
        self.subtitle_tab_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_view.configure(command=self.update_convert_button_state)
        
        # 建立底部通用控制項
        self.controls_frame = create_common_controls(self.root, self)
        self.controls_frame.grid(row=2, column=0, padx=20, pady=(15, 20), sticky="ew")
        
        self.update_epub_ui_state()
        self.update_subtitle_ui_state()

    def set_language(self, lang_code):
        self.current_lang = lang_code
        self._ = lambda s: self.translations[self.current_lang].get(s, s)
        self.update_language()

    def update_language(self):
        self.root.title(self._("app_title"))
        self.app_title_label.configure(text="MayaTransform")
        self.app_subtitle_label.configure(text=self._("subtitle_author"))

        # --- 更新分頁標籤文字的正確方法 ---
        # 1. 取得新的翻譯文字
        new_tab_names = [self._("tab_epub"), self._("tab_subtitle")]
        
        # 2. 直接更新按鈕上顯示的文字
        self.tab_view._segmented_button.configure(values=new_tab_names)
        
        # 3. 更新內部字典的 key，確保與顯示文字同步
        old_keys = list(self.tab_view._name_list)
        for old_key, new_name in zip(old_keys, new_tab_names):
             if old_key != new_name:
                self.tab_view._name_list[self.tab_view._name_list.index(old_key)] = new_name
                self.tab_view._tab_dict[new_name] = self.tab_view._tab_dict.pop(old_key)
                if self.tab_view._current_name == old_key:
                    self.tab_view._current_name = new_name

        # 更新各元件文字
        self.epub_tab_frame.update_language()
        self.subtitle_tab_frame.update_language()

        self.save_path_label.configure(text=self._("save_path"))
        self.choose_location_button.configure(text=self._("choose_location"))
        self.save_path_hint_label.configure(text=self._("save_path_hint"))
        self.convert_button.configure(text=self._("start_conversion"))
        self.status_text.set(self._("status_idle"))
            
        self.update_epub_ui_state()
        self.update_subtitle_ui_state()

    def add_paths_to_epub_queue(self, paths):
        self.epub_tab_frame.add_paths_to_queue(paths)
        
    def update_epub_ui_state(self):
        self.epub_tab_frame.update_ui_state()
        self.update_convert_button_state()

    def add_paths_to_subtitle_queue(self, paths):
        self.subtitle_tab_frame.add_paths_to_queue(paths)

    def update_subtitle_ui_state(self):
        self.subtitle_tab_frame.update_ui_state()
        self.update_convert_button_state()

    def select_output_directory(self):
        dir_path = filedialog.askdirectory(title=self._("choose_location"))
        if dir_path: self.output_dir.set(dir_path)

    def update_convert_button_state(self):
        current_tab_key = self.tab_view.get()
        state = "disabled"
        if current_tab_key == self._("tab_epub") and self.epub_file_queue:
            state = "normal"
        elif current_tab_key == self._("tab_subtitle") and self.subtitle_file_queue:
            state = "normal"
        self.convert_button.configure(state=state)

    def set_ui_lock(self, locked):
        state = "disabled" if locked else "normal"
        self.convert_button.configure(state=state)
        self.epub_tab_frame.set_lock(locked)
        self.subtitle_tab_frame.set_lock(locked)
        self.tab_view.configure(state=state)

    def start_conversion(self):
        current_tab_key = self.tab_view.get()
        self.set_ui_lock(True)
        
        if current_tab_key == self._("tab_epub"):
            if not self.epub_file_queue: 
                self.set_ui_lock(False)
                return
            thread = threading.Thread(target=run_epub_conversion, args=(self.epub_file_queue.copy(), self))
            thread.start()
        elif current_tab_key == self._("tab_subtitle"):
            if not self.subtitle_file_queue: 
                self.set_ui_lock(False)
                return
            thread = threading.Thread(target=run_subtitle_conversion, args=(self.subtitle_file_queue.copy(), self))
            thread.start()

    def conversion_finished(self, total_files):
        self.status_text.set(self._("status_done").format(total_files))
        messagebox.showinfo(self._("done_title"), self._("done_message").format(total_files))
        
        self.status_text.set(self._("status_standby"))
        self.set_ui_lock(False)
        self.update_epub_ui_state()
        self.update_subtitle_ui_state()
