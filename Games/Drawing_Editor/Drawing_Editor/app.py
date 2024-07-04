from tkinter import Tk
from gui import Canvas

class DrawingApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Drawing App")
        self.root.geometry("500x400")
        self.canvas = Canvas(self.root)

    def run(self):
        self.root.mainloop()
