import tkinter as tk
from scenes.panel import Panel

class Panel2(Panel):
    def __init__(self, parent, size):
        self.count = 0
        super().__init__(parent, size, image_path="")

        self.date = "2025-02-04"
        self.belonging_flight = {
            "flight": [
                {
                    "id": "Air-Beijing-Shanghai-2025-03-05-10-25-00",
                    "class": "economy"
                },
                {
                    "id": "Air-Chongqing-Guangzhou-2025-02-05-19-45-00",
                    "class": "first"
                }
            ]
        }

        self.flight_seat = {
            "Air-Beijing-Shanghai-2025-03-05-10-25-00": {
                "first": [
                    [False, True],
                    [False, True],
                    [False, True],
                    [False, False]
                ],
                "business": [
                    [True, True, False, False],
                    [False, False, True, True],
                    [True, True, True, False],
                    [False, True, True, True],
                    [True, True, True, False],
                    [True, True, True, False],
                    [True, True, False, False],
                    [True, False, False, True]
                ],
                "economy": [
                    [True, False, True, True, False, True],
                    [True, False, True, False, True, False],
                    [True, False, True, False, True, False],
                    [True, True, False, False, True, False],
                    [True, True, True, False, False, True],
                    [False, True, True, False, False, True],
                    [True, False, True, False, True, True],
                    [False, False, True, False, True, True],
                    [False, True, False, False, False, True],
                    [True, True, True, False, True, False],
                    [True, True, False, False, False, True],
                    [True, True, False, True, False, True],
                    [True, False, False, True, False, True],
                    [True, True, True, True, False, False],
                    [True, True, True, True, True, True],
                    [False, False, True, False, True, True],
                    [False, True, False, False, True, False],
                    [False, False, True, True, True, False],
                    [True, True, False, False, False, True],
                    [False, False, False, True, False, True],
                    [True, True, True, True, False, False],
                    [False, True, True, True, True, True],
                    [True, True, True, True, False, False],
                    [True, False, True, False, True, False],
                    [False, True, True, True, True, True],
                    [True, False, True, True, False, True],
                    [False, True, True, False, False, False],
                    [True, True, True, False, True, True],
                    [True, False, False, True, False, False],
                    [False, True, True, True, False, True]
                ]
            },
            "Air-Chongqing-Guangzhou-2025-02-05-19-45-00": {
                "first": [
                    [False, False],
                    [True, False],
                    [True, False],
                    [True, False]
                ],
                "business": [
                    [False, False, False, False],
                    [True, False, False, False],
                    [False, True, True, False],
                    [True, False, False, True],
                    [True, True, True, True],
                    [True, False, True, True],
                    [False, False, False, False],
                    [False, True, True, True]
                ],
                "economy": [
                    [True, True, True, False, False, False],
                    [False, True, True, True, False, True],
                    [False, True, True, False, False, True],
                    [True, False, False, False, False, False],
                    [True, False, True, False, False, False],
                    [False, True, True, True, False, True],
                    [True, False, True, True, True, True],
                    [True, False, True, False, True, False],
                    [True, False, False, False, True, True],
                    [False, False, True, True, True, True],
                    [False, True, False, True, False, True],
                    [False, True, False, True, True, True],
                    [False, True, False, False, True, False],
                    [True, True, False, False, False, False],
                    [True, False, False, True, False, True],
                    [True, True, True, False, True, True],
                    [True, True, False, False, True, True],
                    [True, False, True, False, False, True],
                    [True, True, True, False, False, False],
                    [False, False, False, True, False, False],
                    [True, False, False, True, True, False],
                    [True, False, True, False, False, False],
                    [True, False, False, True, False, True],
                    [True, False, False, True, True, True],
                    [True, False, True, False, True, True],
                    [True, False, False, True, True, True],
                    [True, False, True, False, False, True],
                    [True, False, False, False, False, False],
                    [False, False, True, False, True, False],
                    [False, True, False, False, True, False],
                ]
            }
        }

        self.user_info = {
            "flight": None,
            "seat": None
        }


    def update(self):
        if self.voie_text is not None and self.voie_text != "":
            print(self.get_LLM_answer(self.date, self.belonging_flight, self.user_info, self.voie_text))
            self.voie_text = None
            self.parent.start_listening()
        super().update()