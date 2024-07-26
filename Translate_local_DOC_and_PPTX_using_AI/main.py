import customtkinter as ctk
from tkinter import filedialog
import os
from PIL import Image
from TRANSLATE import translate_text_ro_en, translate_text_en_ro
from GRAMMAR import grammar_text_en, grammar_text_ro
from DOC import process_docx
from PPTX import process_slides
import threading


def get_process_function(process, language):
    if process == "grammar":
        if language == "en":
            return grammar_text_en
        elif language == "ro":
            return grammar_text_ro
    elif process == "translate":
        if language == "en_ro":
            return translate_text_en_ro
        elif language == "ro_en":
            return translate_text_ro_en
    return None


def select_file(path_label, success_label, error_label, var_process, var_language):
    file_path = filedialog.askopenfilename(title="Select file:",
                                           filetypes=[("PowerPoint Files", "*.pptx"), ("Word Files", "*.docx")])
    if file_path:
        path_label.delete(0, 'end')  # Șterge textul existent
        path_label.insert(0, file_path)  # Inserează noul text
    else:
        error_label.configure(text="Error: File wasn't selected.", text_color="red")


def process_file(path_label, success_label, error_label, var_process, var_language, progress_bar):
    def run():
        file_path = path_label.get()
        process = var_process.get()
        language = var_language.get()
        process_function = get_process_function(process, language)

        if not process or not language:
            error_label.configure(text="Error: Wasn't selected process or language option.", text_color="red")
            return

        if file_path:
            def set_disabled_text_color(button):
                fg_color = button.cget("fg_color")
                if fg_color == "#D9BA1E":
                    button.configure(state="disabled", text_color_disabled="#223440")
                else:
                    button.configure(state="disabled", text_color_disabled="white")

            error_label.configure(text="")
            success_label.configure(text="Process started:")
            set_disabled_text_color(btn_grammar)
            set_disabled_text_color(btn_translate)
            set_disabled_text_color(btn_ro)
            set_disabled_text_color(btn_en)
            set_disabled_text_color(btn_ro_en)
            set_disabled_text_color(btn_en_ro)
            set_disabled_text_color(select_button)
            set_disabled_text_color(process_button)
            progress_bar.set(0.00001)
            progress_bar.grid(row=7, column=0, columnspan=4, pady=20, padx=(43, 7), sticky="ew")
            root.update_idletasks()
            file_extension = os.path.splitext(file_path)[1].lower()
            final_file = None
            if file_extension == ".pptx":
                final_file = process_slides(file_path, process_function, update_progress_bar)
            elif file_extension == ".docx":
                final_file = process_docx(file_path, process_function, update_progress_bar)

            if final_file:
                success_label.configure(text="The process has been successfully completed.", text_color="green")
                save_file(final_file, file_path, process, language)
            else:
                error_label.configure(text="Error: Process failed.", text_color="red")
        else:
            error_label.configure(text="Error: File wasn't selected.", text_color="red")

    def update_progress_bar(value):
        progress_bar.set(value / 100)
        root.update_idletasks()

    def save_file(final_file, original_file_path, process, language):
        # Extract the original file name without extension
        original_file_name = os.path.basename(original_file_path)
        original_file_name_wo_ext = os.path.splitext(original_file_name)[0]

        # Construct new file name
        if process == "grammar":
            new_file_name = f"{original_file_name_wo_ext}_grammar_{language}.pptx" if original_file_path.endswith(
                ".pptx") else f"{original_file_name_wo_ext}_grammar_{language}.docx"
        elif process == "translate":
            target_language = language.split('_')[-1]
            new_file_name = f"{original_file_name_wo_ext}_translate_{target_language}.pptx" if original_file_path.endswith(
                ".pptx") else f"{original_file_name_wo_ext}_translate_{target_language}.docx"

        # Open the save dialog with the constructed file name
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pptx" if original_file_path.endswith(".pptx") else ".docx",
            filetypes=[("PowerPoint Files", "*.pptx"), ("Word Files", "*.docx")],
            initialfile=new_file_name)
        if save_path:
            final_file.save(save_path)

        path_label.delete(0, 'end')
        select_button.configure(state="normal")
        process_button.configure(state="normal")
        btn_translate.configure(state="normal", text_color="white", fg_color="#223440")
        btn_grammar.configure(state="normal", text_color="white", fg_color="#223440")
        btn_ro.configure(state="normal", text_color="white", fg_color="#223440")
        btn_en.configure(state="normal", text_color="white", fg_color="#223440")
        btn_ro_en.configure(state="normal", text_color="white", fg_color="#223440")
        btn_en_ro.configure(state="normal", text_color="white", fg_color="#223440")

    thread = threading.Thread(target=run)
    thread.start()


def select_process(process_type, buttons, var_process, var_language):
    var_process.set(process_type)
    if process_type == "grammar":
        btn_grammar.configure(fg_color="#D9BA1E", text_color="#223440")
        btn_translate.configure(text_color="white", fg_color="#223440")
        btn_ro.configure(state="normal", text_color="white", fg_color="#223440")
        btn_en.configure(state="normal", text_color="white", fg_color="#223440")
        btn_ro_en.configure(state="disabled", text_color_disabled="gray", fg_color="#223440")
        btn_en_ro.configure(state="disabled", text_color_disabled="gray", fg_color="#223440")
    elif process_type == "translate":
        btn_grammar.configure(text_color="white", fg_color="#223440")
        btn_translate.configure(fg_color="#D9BA1E", text_color="#223440")
        btn_ro.configure(state="disabled", text_color_disabled="gray", fg_color="#223440")
        btn_en.configure(state="disabled", text_color_disabled="gray", fg_color="#223440")
        btn_ro_en.configure(state="normal", text_color="white", fg_color="#223440")
        btn_en_ro.configure(state="normal", text_color="white", fg_color="#223440")


def select_language(language, var_language):
    var_language.set(language)
    if language in ["en"]:
        btn_en.configure(fg_color="#D9BA1E", text_color="#223440")
        btn_ro.configure(fg_color="#223440", text_color="white")
        btn_en_ro.configure(fg_color="#223440", text_color="white")
        btn_ro_en.configure(fg_color="#223440", text_color="white")
    elif language in ["ro"]:
        btn_en.configure(fg_color="#223440", text_color="white")
        btn_ro.configure(fg_color="#D9BA1E", text_color="#223440")
        btn_en_ro.configure(fg_color="#223440", text_color="white")
        btn_ro_en.configure(fg_color="#223440", text_color="white")
    elif language in ["en_ro"]:
        btn_en.configure(fg_color="#223440", text_color="white") 
        btn_ro.configure(fg_color="#223440", text_color="white")
        btn_en_ro.configure(fg_color="#D9BA1E", text_color="#223440")
        btn_ro_en.configure(fg_color="#223440", text_color="white")
    elif language in ["ro_en"]:
        btn_en.configure(fg_color="#223440", text_color="white")
        btn_ro.configure(fg_color="#223440", text_color="white")
        btn_en_ro.configure(fg_color="#223440", text_color="white")
        btn_ro_en.configure(fg_color="#D9BA1E", text_color="#223440")


ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Translator (DOC, PPTX)")
root.resizable(False, False)

frame = ctk.CTkFrame(root)
frame.pack(pady=20)

# Add title label
title_label = ctk.CTkLabel(frame, text="DOCUMENT TRANSLATION", text_color="#223440",
                           font=("Franklin Gothic Heavy", 50, "bold"))
title_label .grid(row=0, column=0,  columnspan=5, padx=20, pady=20)

# Add image to column 0, row 0
image_path = r"/img\doc.png"
image = Image.open(image_path)
image = image.resize((65, 65))  # Resize image as needed
photo = ctk.CTkImage(light_image=image, dark_image=image, size=(65, 65))
image_label = ctk.CTkLabel(frame, image=photo, text="")
image_label.grid(row=2, column=0, rowspan=2, padx=5, pady=5)

# Add image to column 1, row 0
image_path = r"/img\pptx.png"
image = Image.open(image_path)
image = image.resize((65, 65))  # Resize image as needed
photo = ctk.CTkImage(light_image=image, dark_image=image, size=(65, 65))
image_label = ctk.CTkLabel(frame, image=photo, text="")
image_label.grid(row=4, column=0, rowspan=2, padx=5, pady=5)


# ----- File selection
file_select_label = ctk.CTkLabel(frame, text="Selected file:", text_color="#223440", font=("Helvetica", 16, "bold"))
file_select_label.grid(row=1, column=0, padx=20)

path_label = ctk.CTkEntry(frame, width=50, text_color="#223440", border_color="#223440", bg_color="white")
path_label.grid(row=1, column=1, columnspan=3, padx=5, sticky="we")

select_button = ctk.CTkButton(frame, text="Select", fg_color="#223440", font=("Helvetica", 16, "bold"),
                              command=lambda: select_file(path_label, success_label, error_label, var_process,
                                                          var_language))
select_button.grid(row=1, column=4, padx=30, pady=5, sticky="nsew")

# ----- Process selection
var_process = ctk.StringVar()
btn_grammar = ctk.CTkButton(frame, text="Grammar", fg_color="#223440", font=("Helvetica", 18, "bold"),
                            command=lambda: select_process("grammar", [btn_ro, btn_en], var_process, var_language))
btn_grammar.grid(row=2, column=1, rowspan=2, columnspan=2, padx=5, pady=(20, 5), sticky="nsew")

btn_translate = ctk.CTkButton(frame, text="Translate", fg_color="#223440",  font=("Helvetica", 18, "bold"),
                              command=lambda: select_process("translate", [btn_ro_en, btn_en_ro], var_process,
                                                             var_language))
btn_translate.grid(row=4, column=1, rowspan=2, columnspan=2, padx=5, pady=5, sticky="nsew")


# ----- Language selection
var_language = ctk.StringVar()
btn_ro = ctk.CTkButton(frame, text="Romanian", fg_color="#223440", font=("Helvetica", 14, "bold"), state="disabled",
                       command=lambda: select_language("ro", var_language))
btn_ro.grid(row=2, column=3, padx=5, pady=(20, 5), sticky="nsew")

btn_en = ctk.CTkButton(frame, text="English", fg_color="#223440", font=("Helvetica", 14, "bold"), state="disabled",
                       command=lambda: select_language("en", var_language))
btn_en.grid(row=3, column=3, padx=5, pady=5, sticky="nsew")

btn_ro_en = ctk.CTkButton(frame, text="RO > EN", fg_color="#223440", font=("Helvetica", 14, "bold"), state="disabled",
                          text_color="white", command=lambda: select_language("ro_en", var_language))
btn_ro_en.grid(row=4, column=3, padx=5, pady=5, sticky="nsew")

btn_en_ro = ctk.CTkButton(frame, text="EN > RO", fg_color="#223440", font=("Helvetica", 14, "bold"), state="disabled",
                          command=lambda: select_language("en_ro", var_language))
btn_en_ro.grid(row=5, column=3, padx=5, pady=5, sticky="nsew")

# ----- Status labels
error_label = ctk.CTkLabel(frame, text="", text_color="red", font=("Helvetica", 12, "bold"))
error_label.grid(row=6, column=1, columnspan=3)

success_label = ctk.CTkLabel(frame, text="", text_color="green", font=("Helvetica", 12, "bold"))
success_label.grid(row=6, column=1, columnspan=3)

# Process file button
process_button = ctk.CTkButton(frame, text="Start", fg_color="#223440", font=("Helvetica", 16, "bold"),
                               command=lambda: process_file(path_label, success_label, error_label, var_process,
                                                            var_language, progress_bar))
process_button.grid(row=7, column=4, padx=30, pady=5, sticky="nsew")

# Progress bar
progress_bar = ctk.CTkProgressBar(frame, orientation="horizontal", fg_color="white", border_width=2,
                                  progress_color="#223440", border_color="#223440",
                                  height=25, mode="determinate")
progress_bar.set(0.00001)  # Set the initial value to 0
progress_bar.grid(row=7, column=0, columnspan=4, pady=20,  padx=(43, 7), sticky="ew")

root.mainloop()
