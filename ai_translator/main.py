import sys
import os
import tkinter as tk

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator
from tkinter import filedialog
from pdf2image import convert_from_path
from PIL import ImageTk, Image

filename = "" 
def translate_pdf(args, language: str, file_path: str, output_file_path: str):
    
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    if args.model_type == "OpenAIModel":
        model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
        api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
        model = OpenAIModel(model=model_name, api_key=api_key)
    elif args.model_type == "GLMModel":
        timeout = args.timeout if args.timeout else config['GLMModel']['timeout']
        model_url = args.model_url if args.model_url else config['GLMModel']['model_url']
        model = GLMModel(model_url=model_url, timeout=timeout)
    else:
        raise ValueError("Invalid model_type specified. Please choose either 'GLMModel' or 'OpenAIModel'.")


    pdf_file_path = file_path

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(file_path, 'markdown', language, output_file_path)

def start_gui():
    parser = ArgumentParser()

    args = parser.parse_arguments()

    def upload_action(event=None):
        global filename
        global file_extension
        filename = filedialog.askopenfilename()

        # Update the label with the file path
        file_path_label.config(text=f'上传文件: {filename}')

    def start_translation(event=None):
        global filename
        if filename == None or filename == "" :
            print('The selected file is not a PDF.')
            # Update the label with the warning
            file_path_label.config(text=f'请上传文件后再进行翻译')
            return

        # Get the file extension
        _, file_extension = os.path.splitext(filename)

        if file_extension != '.pdf':
            print('The selected file is not a PDF.')
            # Update the label with the warning
            file_path_label.config(text=f'上传文件不是PDF格式')
            return
        # Get the selected language
        selected_language = language_var.get()

        # Ask the user to select a directory
        output_directory = filedialog.askdirectory()
        print('Selected directory:', output_directory)

        # Create a file path with a specific file name in the selected directory
        output_file_path = os.path.join(output_directory, 'translated.md')


        print(f'Selected:{filename} language:{selected_language}')
        translate_pdf(args, selected_language,filename,output_file_path)


    root = tk.Tk()
    root.geometry("800x600")
    root.title("PDF AI Translator")

    # Create a label for the file path
    file_path_label = tk.Label(root, text="")
    file_path_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # Create a dropdown menu for language selection
    languages = ['English', '中文', 'Español', 'Français', 'Deutsch']
    language_var = tk.StringVar(root)
    language_var.set(languages[0])  # set the default option
    language_dropdown = tk.OptionMenu(root, language_var, *languages)
    language_dropdown.place(relx=0.46, rely=0.5, anchor=tk.CENTER)


    button = tk.Button(root, text='Upload PDF', command=upload_action)
    button.place(relx=0.34, rely=0.5, anchor=tk.CENTER)

    # Create a button to start translation
    button_translate = tk.Button(root, text='Start Translation', command=start_translation)
    button_translate.place(relx=0.6, rely=0.5, anchor=tk.CENTER)


    root.mainloop()

# Call the function to start the GUI
start_gui()
