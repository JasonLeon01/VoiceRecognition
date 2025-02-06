import tkinter as tk
from tkinter import PhotoImage
from scenes.panel1 import Panel1

class App:
    def __init__(self, root, size):
        self.root = root
        self.root.title('Voice Recognition System')
        self.current_page = 0
        self.panels = []

        self.panels.append(Panel1(self.root, size))

        self.panels[self.current_page].show()

        self.root.bind('<space>', self.next_page)
        self.root.bind('<MouseWheel>', self.on_mouse_wheel)

    def next_page(self, event=None):
        self.panels[self.current_page].hide()
        self.current_page = (self.current_page + 1) % len(self.panels)
        self.panels[self.current_page].show()

    def prev_page(self, event=None):
        self.panels[self.current_page].hide()
        self.current_page = (self.current_page - 1) % len(self.panels)
        self.panels[self.current_page].show()

    def on_mouse_wheel(self, event):
        if event.delta > 0:  # 向上滚动
            self.prev_page()
        else:  # 向下滚动
            self.next_page()

def main():
    root = tk.Tk()
    size = (800, 600)
    root.geometry(f"{size[0]}x{size[1]}")
    app = App(root, size)
    root.mainloop()

if __name__ == '__main__':
    main()