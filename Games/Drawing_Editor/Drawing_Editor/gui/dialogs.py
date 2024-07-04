from tkinter import filedialog
from tkinter import simpledialog
import tkinter as tk

class OpenFileDialog:
    @staticmethod
    def show():
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        return file_path

class SaveFileDialog:
    @staticmethod
    def show():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        return file_path

class ExportDialog:
    @staticmethod
    def show(file_types, default_extension):
        file_path = filedialog.asksaveasfilename(defaultextension=default_extension, filetypes=file_types)
        return file_path


class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, shape_type):
        self.shape_type = shape_type
        super().__init__(parent)

    def body(self, master):
        tk.Label(master, text="Enter line color:").grid(row=0, column=0, sticky="w")
        self.line_color_var = tk.StringVar()
        self.line_color_var.set("black")  # Set the default value
        self.line_color_menu = tk.OptionMenu(master, self.line_color_var, "black", "red", "green", "blue")
        self.line_color_menu.grid(row=0, column=1)

        if self.shape_type == "rectangle":
            tk.Label(master, text="Enter corner style:").grid(row=1, column=0, sticky="w")
            self.corner_style_var = tk.StringVar()
            self.corner_style_var.set("square")  # Set the default value
            self.corner_style_menu = tk.OptionMenu(master, self.corner_style_var, "square", "rounded")
            self.corner_style_menu.grid(row=1, column=1)

        return self.line_color_menu  # Return the line color OptionMenu to make it the initial focus

    def apply(self):
        self.line_color = self.line_color_var.get()
        if self.shape_type == "rectangle":
            self.corner_style = self.corner_style_var.get()