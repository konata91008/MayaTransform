import os
import opencc
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from tkinter import messagebox

def get_output_path(output_dir, source_path, suffix):
    base, ext = os.path.splitext(os.path.basename(source_path))
    if output_dir:
        return os.path.join(output_dir, f"{base}{suffix}{ext}")
    else:
        return os.path.join(os.path.dirname(source_path), f"{base}{suffix}{ext}")

def run_epub_conversion(paths_to_convert, controller):
    selected_config_name = controller.epub_conversion_direction.get()
    config_file = controller.translations[controller.current_lang]['epub_conversion_options'].get(selected_config_name)
    
    if not config_file:
        controller.root.after(0, messagebox.showerror, "Config Error", "Could not find config for EPUB conversion.")
        controller.root.after(0, controller.conversion_finished, 0)
        return

    cc = opencc.OpenCC(config_file)
    
    output_dir = controller.output_dir.get()
    total_files = len(paths_to_convert)

    for i, path in enumerate(paths_to_convert):
        filename = os.path.basename(path)
        controller.root.after(0, controller.status_text.set, controller._("status_processing").format(i + 1, total_files, filename))
        try:
            suffix = "_tw" if "t2s" not in config_file else "_cn"
            output_path = get_output_path(output_dir, path, suffix)

            book = epub.read_epub(path)
            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                html_content = item.get_content().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html_content, 'html.parser')
                text_nodes = soup.find_all(string=True)
                for text_node in text_nodes:
                    if text_node.parent.name in ['style', 'script', 'title']: continue
                    converted_text = cc.convert(str(text_node))
                    text_node.replace_with(converted_text)
                item.set_content(str(soup).encode('utf-8'))
            epub.write_epub(output_path, book, {})
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            controller.root.after(0, messagebox.showerror, controller._("error_title"), controller._("error_message").format(filename, e))
            
    controller.root.after(0, controller.conversion_finished, total_files)
