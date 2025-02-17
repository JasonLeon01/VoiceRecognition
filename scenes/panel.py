import os
import tkinter as tk
from tkinter import PhotoImage
from sentence_transformers import SentenceTransformer, util

# path: C:\Users\username\.cache\huggingface\hub\models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2
class Panel(tk.Frame):
    sentence_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    def __init__(self, parent, size, image_path=None):
        self.parent = parent
        width, height = size
        super().__init__(parent.root, width=width, height=height)
        self.voie_text = None
        self.next_panel = None

        self.bg_image = PhotoImage(file=image_path)
        self.bg_label = tk.Label(master=self, image=self.bg_image)
        self.bg_label.place(x=0, y=0)

        self.fg_label = tk.Label(master=self, text="", font=("Arial", 24))
        self.fg_label.place(x=50, y=50)
        self._update_id = None

    def get_model(self):
        return Panel.sentence_model

    def get_text(self, text):
        self.voie_text = text
        self.fg_label.config(text=text)

    def update(self):
        # 基类内容，后面通过super调用
        self._update_id = self.after(16, self.update)
        
    def show(self):
        self.place(x=0, y=0)
        if self._update_id is None:
            self.update()
        
    def hide(self):
        self.place_forget()
        if self._update_id:
            self.after_cancel(self._update_id)
            self._update_id = None

    def next_node(self):
        self.hide()
        self.parent.current_panel = self.next_panel
        self.parent.current_panel.show()
        self.parent.start_listening()

    def extract_information(self, text: str, sentence: dict):
        text_embedding = self.get_model().encode(text)
        instruction_texts = list(sentence.keys())
        instruction_embeddings = self.get_model().encode(instruction_texts)
        similarities = util.pytorch_cos_sim(text_embedding, instruction_embeddings)

        best_match_index = similarities.argmax().item()
        best_match_score = similarities[0, best_match_index].item()
        best_match_instruction = instruction_texts[best_match_index]
        return best_match_score, best_match_instruction
