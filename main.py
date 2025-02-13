import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'Resemblyzer'))
import tkinter as tk
import VoiceWatch
from scenes.panel import Panel
from scenes.panel1 import Panel1
from scenes.panel2 import Panel2

class App:
    def __init__(self, root, size):
        self.root = root
        self.root.title('Voice Recognition System')

        self.listener = VoiceWatch.Listener("航班助手", lambda text: root.after(0, self.response, text))
        self.listener.start_listening()

        self._panel1 = Panel1(self, size)
        self._panel2 = Panel2(self, size)
        self._panel1.next_panel = self._panel2
        self._panel2.next_panel = self._panel1

        self.current_page: Panel = self._panel1

        self.current_page.show()
        self.start_listening()

    def start_listening(self):
        self.listener.start_listening()

    def stop_listening(self):
        self.listener.stop_listening()

    def response(self, text=None):
        if text is not None:
            self.current_page.get_text(text)

def main():
    root = tk.Tk()
    size = (800, 600)
    root.geometry(f"{size[0]}x{size[1]}")
    app = App(root, size)
    root.mainloop()

if __name__ == '__main__':
    main()