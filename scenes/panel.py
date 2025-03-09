import os
import tkinter as tk
from tkinter import PhotoImage
import LLM

class Panel(tk.Frame):
    def __init__(self, parent, size, image_path=None):
        self.parent = parent
        width, height = size
        super().__init__(parent.root, width=width, height=height)
        self.voie_text = None
        self.next_panel = None

        self.bg_image = PhotoImage(file=image_path)
        self.bg_label = tk.Label(master=self, image=self.bg_image)
        self.bg_label.place(x=0, y=0)

        self.fg_label = tk.Label(
            master=self,
            text="",
            font=("Arial", 24),
            wraplength=width - 100,  # 设置换行宽度，留出左右边距
            justify="left"           # 换行后文字左对齐
        )
        self.fg_label.place(x=50, y=50)
        self._update_id = None

    def get_text(self, text, NPS):
        if NPS == False:
            self.fg_label.config(text=text)
        self.voie_text = text

    def clear_text(self):
        self.voie_text = None
        self.fg_label.config(text="")

    def update(self):
        # 基类内容，后面通过super调用
        if self._update_id == -1:
            return
        else:
            self._update_id = self.after(16, self.update)
        
    def show(self):
        self.place(x=0, y=0)
        if self._update_id is None:
            self.update()
        
    def hide(self):
        self.place_forget()
        if self._update_id:
            self.after_cancel(self._update_id)
            self._update_id = -1

    def next_node(self):
        self.hide()
        self.parent.current_panel = self.next_panel
        self.parent.current_panel.show()

    def get_LLM_answer(self, date, belonging_flight, user_info, dialogue):
        return LLM.LLM.get_flight_info(date, belonging_flight, user_info, dialogue)