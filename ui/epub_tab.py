import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import tkinterdnd2 as TkinterDnD

class EpubTab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        # --- 關鍵修正：設定框架的背景顏色，不再使用透明色 ---
        light_bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0]
        super().__init__(parent, fg_color=light_bg_color, corner_radius=0)
        
        self.controller = controller
        self._ = self.controller._

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # --- 頂部操作區 (使用 grid 精確對齊) ---
        list_actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        list_actions_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        list_actions_frame.columnconfigure(2, weight=1)

        self.add_button = ctk.CTkButton(list_actions_frame, command=self.add_files_dialog)
        self.add_button.grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.remove_button = ctk.CTkButton(list_actions_frame, command=self.remove_selected_files)
        self.remove_button.grid(row=0, column=1, sticky="w")
        
        count_label = ctk.CTkLabel(list_actions_frame, textvariable=self.controller.epub_file_count_text)
        count_label.grid(row=0, column=3, sticky="e")

        # --- 檔案列表框 ---
        self.file_listbox = tk.Listbox(self, 
            selectmode=tk.EXTENDED, 
            font=("Segoe UI", 11),
            bg="#FFFFFF", fg="#212529",
            selectbackground="#3B8ED0", selectforeground="white",
            relief="solid", borderwidth=1,
            highlightthickness=1,
            highlightbackground="#D5D5D5", highlightcolor="#3B8ED0"
        )
        self.file_listbox.grid(row=1, column=0, sticky="nsew", pady=5)
        
        self.file_listbox.drop_target_register(TkinterDnD.DND_FILES)
        self.file_listbox.dnd_bind('<<Drop>>', self.handle_drop)
        
        # --- 底部選項區 ---
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.grid(row=2, column=0, sticky="ew", pady=(10,0))
        
        self.direction_label = ctk.CTkLabel(options_frame)
        self.direction_label.pack(side="left", padx=(0, 10))
        
        self.direction_combo = ctk.CTkComboBox(options_frame, variable=self.controller.epub_conversion_direction, state="readonly", width=300)
        self.direction_combo.pack(side="left")

    def update_language(self):
        self.add_button.configure(text=self._("import_files"))
        self.remove_button.configure(text=self._("remove_selected"))
        self.direction_label.configure(text=self._("conversion_direction"))
        
        options = list(self._("epub_conversion_options").keys())
        self.direction_combo.configure(values=options)
        if self.controller.epub_conversion_direction.get() not in options:
            self.controller.epub_conversion_direction.set(options[0])

    def add_files_dialog(self):
        paths = filedialog.askopenfilenames(
            title=self._("select_epub_files"),
            filetypes=[(self._("epub_file_type"), "*.epub")]
        )
        if paths: self.add_paths_to_queue(paths)

    def handle_drop(self, event):
        paths = self.winfo_toplevel().tk.splitlist(event.data)
        self.add_paths_to_queue(paths)
        return event.action

    def add_paths_to_queue(self, paths):
        for path in paths:
            if path.lower().endswith('.epub') and path not in self.controller.epub_file_queue:
                self.controller.epub_file_queue.append(path)
                self.file_listbox.insert(tk.END, path)
        self.controller.update_epub_ui_state()

    def remove_selected_files(self):
        selected_indices = self.file_listbox.curselection()
        for i in sorted(selected_indices, reverse=True):
            self.file_listbox.delete(i)
            del self.controller.epub_file_queue[i]
        self.controller.update_epub_ui_state()

    def update_ui_state(self):
        count = len(self.controller.epub_file_queue)
        self.controller.epub_file_count_text.set(self._("total_files").format(count))
        state = "normal" if count > 0 else "disabled"
        self.remove_button.configure(state=state)

    def set_lock(self, locked):
        state = "disabled" if locked else "normal"
        self.add_button.configure(state=state)
        self.remove_button.configure(state="normal" if len(self.controller.epub_file_queue) > 0 and not locked else "disabled")
        self.direction_combo.configure(state="readonly" if not locked else "disabled")
