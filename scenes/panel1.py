import re
import tkinter as tk
from scenes.panel import Panel

class Panel1(Panel):
    def __init__(self, parent, size):
        self.count = 0
        super().__init__(parent, size, image_path="bg/1.png")
        self.sentence = {
            "select_seat": "选择x的第y排第z个座位",
            "book_meal": "预订x餐食"
        }
        self.start_counting = False

    def update(self):
        if self.count >= 100:
            self.count = 0
            if self.next_panel:
                self.next_node()

        if self.start_counting:
            self.count += 1
        
        if self.voie_text is not None:
            print("Extracting information from sentence...")

            print(self.voie_text)

            self.voie_text = None
            self.parent.start_listening()

        super().update()
