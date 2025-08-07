import os
import re
import opencc
from tkinter import messagebox

def get_output_path(output_dir, source_path, suffix):
    base, ext = os.path.splitext(os.path.basename(source_path))
    if output_dir:
        return os.path.join(output_dir, f"{base}{suffix}{ext}")
    else:
        return os.path.join(os.path.dirname(source_path), f"{base}{suffix}{ext}")

def run_subtitle_conversion(paths_to_convert, controller):
    selected_config_name = controller.subtitle_conversion_direction.get()
    config_file = controller.translations[controller.current_lang]['subtitle_conversion_options'].get(selected_config_name)

    if not config_file:
        controller.root.after(0, messagebox.showerror, "Config Error", "Could not find config for subtitle conversion.")
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

            with open(path, 'r', encoding='utf-8-sig') as f_in, \
                 open(output_path, 'w', encoding='utf-8') as f_out:
                if path.lower().endswith('.srt'):
                    for line in f_in:
                        if '-->' not in line and not re.match(r'^\d+$', line.strip()):
                            f_out.write(cc.convert(line))
                        else:
                            f_out.write(line)
                elif path.lower().endswith('.ass'):
                     for line in f_in:
                        if line.strip().startswith('Dialogue:'):
                            parts = line.split(',', 9)
                            if len(parts) == 10:
                                parts[9] = cc.convert(parts[9])
                                f_out.write(','.join(parts))
                            else:
                                f_out.write(line)
                        else:
                            f_out.write(line)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            controller.root.after(0, messagebox.showerror, controller._("error_title"), controller._("error_message").format(filename, e))
            
    controller.root.after(0, controller.conversion_finished, total_files)
