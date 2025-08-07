import customtkinter as ctk

def create_header(parent, controller):
    # --- 頂部標題區 ---
    header_frame = ctk.CTkFrame(parent, fg_color="transparent")
    header_frame.grid(row=0, column=0, sticky="ew")
    header_frame.columnconfigure(0, weight=1)
    
    title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    title_frame.grid(row=0, column=0, sticky="w")
    
    controller.app_title_label = ctk.CTkLabel(title_frame, text="", font=ctk.CTkFont(size=20, weight="bold"))
    controller.app_title_label.pack(anchor="w")
    # 移除寫死的顏色，讓 CustomTkinter 自動根據主題配色
    controller.app_subtitle_label = ctk.CTkLabel(title_frame, text="")
    controller.app_subtitle_label.pack(anchor="w")

    # --- 語言切換按鈕區 ---
    lang_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    lang_frame.grid(row=0, column=1, sticky="e")
    
    ctk.CTkButton(lang_frame, text="繁體中文", width=100, command=lambda: controller.set_language("zh_TW")).pack(side="left", padx=(0,5))
    ctk.CTkButton(lang_frame, text="English", width=100, command=lambda: controller.set_language("en")).pack(side="left", padx=(0,5))
    ctk.CTkButton(lang_frame, text="日本語", width=100, command=lambda: controller.set_language("jp")).pack(side="left")
    
    return header_frame

def create_common_controls(parent, controller):
    # --- 主要容器，使用 pack 來管理內部的 settings_card 和 footer_frame ---
    container = ctk.CTkFrame(parent, fg_color="transparent")

    # --- 儲存路徑設定卡片 ---
    settings_card = ctk.CTkFrame(container, corner_radius=8)
    settings_card.pack(fill="x", expand=True, side="top")
    settings_card.columnconfigure(1, weight=1) # 讓中間的輸入框欄位可以擴展
    
    controller.save_path_label = ctk.CTkLabel(settings_card, text="")
    controller.save_path_label.grid(row=0, column=0, sticky="w", padx=15, pady=15)

    output_entry = ctk.CTkEntry(settings_card, textvariable=controller.output_dir)
    output_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=15)

    controller.choose_location_button = ctk.CTkButton(settings_card, text="", width=100, command=controller.select_output_directory)
    controller.choose_location_button.grid(row=0, column=2, sticky="e", padx=15, pady=15)
    
    # 移除寫死的顏色，讓 CustomTkinter 自動根據主題配色
    controller.save_path_hint_label = ctk.CTkLabel(settings_card, text="")
    controller.save_path_hint_label.grid(row=1, column=1, columnspan=2, sticky="w", padx=0, pady=(0,15))

    # --- 底部狀態列與開始按鈕 ---
    footer_frame = ctk.CTkFrame(container, fg_color="transparent")
    footer_frame.pack(fill="x", expand=True, side="bottom", pady=(15, 0))
    footer_frame.columnconfigure(0, weight=1)
    
    # 移除寫死的顏色，讓 CustomTkinter 自動根據主題配色
    controller.status_label = ctk.CTkLabel(footer_frame, textvariable=controller.status_text)
    controller.status_label.grid(row=0, column=0, sticky="w")
    
    controller.convert_button = ctk.CTkButton(footer_frame, text="", font=ctk.CTkFont(size=14, weight="bold"), command=controller.start_conversion)
    controller.convert_button.grid(row=0, column=1, sticky="e")
    
    return container
