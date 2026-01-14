import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


from .animated_gif import AnimatedGIF
from Other.utils import resource_path

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Color me clean!")
        self.resizable(False, False)

if __name__ == "__main__":
    pass