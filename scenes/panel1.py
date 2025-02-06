import tkinter as tk
from scenes.panel import Panel

class Panel1(Panel):
    def __init__(self, parent, size):
        super().__init__(parent, size, image_path="bg/GrassBackground.png")

        label = tk.Label(self.frame, text="这是第一个面板")
        label.place(x=50, y=50)