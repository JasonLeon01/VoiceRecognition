import sys
import os
import tkinter as tk
from typing import List
sys.path.append(os.path.join(os.getcwd(), 'Resemblyzer'))
import VoiceWatch
from scenes.panel import Panel
from scenes.panel1 import Panel1
from scenes.panel2 import Panel2
from scenes.panel3 import Panel3
from scenes.panel4 import Panel4
from scenes.panel5 import Panel5
from scenes.panel6 import Panel6
from scenes.panel7 import Panel7
from scenes.panel8 import Panel8
from scenes.panel9 import Panel9
from scenes.panel10 import Panel10
from scenes.panel11 import Panel11
from scenes.panel12 import Panel12
from scenes.panel13 import Panel13
from scenes.panel14 import Panel14
from scenes.panel15 import Panel15
from scenes.panel16 import Panel16
from scenes.panel17 import Panel17
from scenes.panel18 import Panel18
from scenes.panel19 import Panel19
from scenes.panel20 import Panel20
from scenes.panel21 import Panel21
from scenes.panel22 import Panel22
from scenes.panel23 import Panel23

class App:
    def __init__(self, root, size):
        self.root = root
        self.root.title('Voice Recognition System')

        self.listener = VoiceWatch.Listener("航班助手", lambda text: root.after(0, self.response, text))
        self.listener.start_listening()

        self.panels: List[Panel] = [Panel1(self, size), Panel2(self, size), Panel3(self, size), Panel4(self, size), Panel5(self, size), Panel6(self, size), Panel7(self, size), Panel8(self, size), Panel9(self, size), Panel10(self, size), Panel11(self, size), Panel12(self, size), Panel13(self, size), Panel14(self, size), Panel15(self, size), Panel16(self, size), Panel17(self, size), Panel18(self, size), Panel19(self, size), Panel20(self, size), Panel21(self, size), Panel22(self, size), Panel23(self, size)]
        for i in range(len(self.panels) - 1):
            self.panels[i].next_panel = self.panels[(i + 1) % len(self.panels)]

        self.current_page: Panel = self.panels[0]

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