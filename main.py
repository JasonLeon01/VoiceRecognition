import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'Resemblyzer'))
import tkinter as tk
from typing import List
import VoiceWatch
from scenes.panel import Panel
from scenes.panel1 import Panel1
from scenes.panel2 import Panel2
from scenes.panel3 import Panel3
from scenes.panel4 import Panel4
from scenes.panel5 import Panel5
from scenes.panel6 import Panel6

class App:
    def __init__(self, root, size):
        self.root = root
        self.root.title('Voice Recognition System')

        self.listener = VoiceWatch.Listener(lambda text: root.after(0, self.response, text))

        self.panels: List[Panel] = [Panel1(self, size), Panel2(self, size), Panel3(self, size), Panel4(self, size), Panel5(self, size), Panel6(self, size)]
        for i in range(len(self.panels) - 1):
            self.panels[i].next_panel = self.panels[(i + 1) % len(self.panels)]

        self.current_panel: Panel = self.panels[0]

        self.current_panel.show()
        self.start_listening()

    def start_listening(self):
        self.listener.start_listening()

    def stop_listening(self):
        self.listener.stop_listening()

    def response(self, text=None):
        if text is not None and text != "":
            self.current_panel.get_text(text, False)
        else:
            self.current_panel.get_text("", True)
            self.start_listening()

def main():
    root = tk.Tk()
    size = (800, 600)
    root.geometry(f"{size[0]}x{size[1]}")
    app = App(root, size)
    root.mainloop()

if __name__ == '__main__':
    main()