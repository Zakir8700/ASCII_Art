import os
import shutil
import threading
from tkinter import Tk, Button, Label, filedialog, messagebox
from tkinter.ttk import Progressbar
from datetime import datetime
import time
import Image_to_ASCII
from dotenv import load_dotenv, find_dotenv

load_dotenv()
root_dir = os.path.dirname(find_dotenv())

timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
UPLOAD_DIR = os.path.join(root_dir, os.getenv("Folder_path"))

os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to ASCII Converter")
        self.root.geometry("450x220")
        self.root.configure(bg="lightgray")
        self.RESULT_DIR = os.path.join(os.path.join(root_dir, os.getenv("Output_path")), timestamp)

        self.label = Label(root, text="Select one or more files to upload and process:")
        self.label.configure(bg="lightgray")
        self.label.pack(pady=10)

        self.select_btn = Button(root, text="Select Files", command=self.select_files)
        self.select_btn.pack(pady=5)

        self.progress = Progressbar(root, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["value"] = 0

        self.open_results_btn = Button(root, text="Open Results Folder", command=self.open_results_folder, state="disabled")
        self.open_results_btn.pack(pady=5)

    def select_files(self):
        filepaths = filedialog.askopenfilenames(title="Select files")
        if filepaths:
            self.process_files(filepaths)

    def process_files(self, filepaths):
        self.progress["value"] = 0
        self.open_results_btn.config(state="disabled")
        thread = threading.Thread(target=self._process_files_thread, args=(filepaths,))
        thread.start()

    def _process_files_thread(self, filepaths):
        try:
            total_files = len(filepaths)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
            for idx, filepath in enumerate(filepaths):
                filename = os.path.basename(filepath)
                upload_path = os.path.join(UPLOAD_DIR, filename)
                shutil.copy(filepath, upload_path)
                self.RESULT_DIR = os.path.join(os.path.join(root_dir, os.getenv("Output_path")), timestamp)
                os.makedirs(self.RESULT_DIR, exist_ok=True)

                #file processing delay
                time.sleep(1)
                Image_to_ASCII.ascii_converter(self.RESULT_DIR)

                # Update progress
                progress_value = ((idx + 1) / total_files) * 100
                self.progress["value"] = progress_value
                self.root.update_idletasks()

            self.open_results_btn.config(state="normal")
            messagebox.showinfo("Success", "All files processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def open_results_folder(self):
        if os.path.exists(self.RESULT_DIR):
            os.startfile(self.RESULT_DIR)
        else:
            messagebox.showwarning("Warning", "Results folder not found!")

if __name__ == "__main__":
    root = Tk()
    app = FileProcessorApp(root)
    root.mainloop()
