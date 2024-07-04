from tkinter import *

class Color:
    def __init__(self):
        self.supported_colors = {
            "black": "k",
            "red": "r",
            "green": "g",
            "blue": "b",
        }

    def get_color_code(self, color_name):
        return self.supported_colors.get(color_name, "k")

    def get_color_name(self, color_code):
        for name, code in self.supported_colors.items():
            if code == color_code:
                return name
        return "black"

    def get_color_options(self):
        return list(self.supported_colors.keys())

class ColorManager(Color):
    def __init__(self, root):
        super().__init__()
        self.color = "black"
        self.selected_color = StringVar(value="black")

        color_menu = OptionMenu(root, self.selected_color, *self.get_color_options())
        color_menu.pack(side="top", padx=40, pady=10)

        self.selected_color.trace("w", lambda *args: self.choose_color())

    def choose_color(self):
        self.color = self.selected_color.get()