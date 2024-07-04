import tkinter
from tkinter import *
from tkinter import ttk
class Buttons:
    def __init__(self, root, drawing_app):
        self.active_button = None
        self.drawing_app = drawing_app

        self.rect_button = tkinter.Button(text="Rectangle", command=lambda: drawing_app.set_brush_type("rectangle"))
        self.rect_button.pack(side="top", padx=10, pady=10)
        self.rect_button2 = tkinter.Button(text="Rounded Rectangle", command=lambda: drawing_app.set_brush_type("rounded_rectangle"))
        self.rect_button2.pack(side="top", padx=10, pady=10)
        self.line_button = tkinter.Button(text="Line", command=lambda: drawing_app.set_brush_type("line"))
        self.line_button.pack(side="top", padx=10, pady=10)
        self.select_button = tkinter.Button(text="Arrow", command=lambda: drawing_app.set_brush_type("arrow"))
        self.select_button.pack(side="top", padx=10, pady=10)
        self.delete_button = tkinter.Button(text="Delete", command=drawing_app.delete_object)
        self.delete_button.pack(side="top", padx=10, pady=10)
        self.size_button = Scale(label="Thickness", from_=3, to=10, orient=HORIZONTAL)
        self.size_button.pack(side="top", padx=10, pady=10)
        self.copy_button = tkinter.Button(text="Copy", command=drawing_app.copy_objects)
        self.copy_button.pack(side="top", padx=10, pady=10)
        self.paste_button = tkinter.Button(text="Paste", command=drawing_app.paste_objects)
        self.paste_button.pack(side="top", padx=10, pady=10)
        self.group_button = tkinter.Button(text="Group", command=drawing_app.group_objects)
        self.group_button.pack(side="top", padx=10, pady=10)
        self.ungroup_button = tkinter.Button(text="Ungroup", command=drawing_app.ungroup_objects)
        self.ungroup_button.pack(side="top", padx=10, pady=10)
        self.ungroup_all_button = tkinter.Button(text="Ungroup All", command=drawing_app.ungroup_all)
        self.ungroup_all_button.pack(side="top", padx=10, pady=10)
        self.edit_button = tkinter.Button(text="Edit", command=drawing_app.edit_selected_object)
        self.edit_button.pack(side="top", padx=10, pady=10)