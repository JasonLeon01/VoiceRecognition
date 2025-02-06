import tkinter as tk
from tkinter import PhotoImage

class Panel:
    def __init__(self, parent, size, image_path=None):
        self.parent = parent
        self.frame = tk.Frame(parent)
        width, height = size
        if image_path:
            self.image = PhotoImage(file=image_path)
            self.canvas = tk.Canvas(self.frame, width=width, height=height)
            self.canvas.pack(fill=tk.BOTH, expand=True)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        else:
            self.canvas = None
        
    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        
    def hide(self):
        self.frame.pack_forget()