import tkinter as tk
from scenes.panel import Panel

class Panel9(Panel):
    def __init__(self, parent, size):
        self.count = 0
        super().__init__(parent, size, image_path="bg/9.png")

    def update(self):
        if self.count >= 100:
            self.count = 0
            if self.next_panel:
                self.next_node()
        self.count += 1
        super().update()