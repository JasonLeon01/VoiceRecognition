import tkinter as tk
from scenes.panel import Panel

class Panel2(Panel):
    def __init__(self, parent, size):
        self.count = 0
        super().__init__(parent, size, image_path="bg/2.png")

    def update(self):
        if self.count >= 1000:
            self.count = 0
            if self.next_panel:
                self.next_node()
        self.count += 1
        super().update()