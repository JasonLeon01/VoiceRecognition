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
            "flight": "None",
            "seat": "None"
        }

        # 航班信息显示
        self.flight_label = tk.Label(self, text="当前选择航班：None", font=('Arial', 12))
        self.flight_label.place(relx=0.5, rely=0.3, anchor='center')
        
        # 座位信息显示
        self.seat_label = tk.Label(self, text="当前选择座位：None", font=('Arial', 12))
        self.seat_label.place(relx=0.5, rely=0.4, anchor='center')
        
        # 查看航班按钮
        self.view_flights_btn = tk.Button(self, text="查看名下航班", font=('Arial', 10))
        self.view_flights_btn.place(relx=0.5, rely=0.5, anchor='center')
        
        # 查看座位按钮
        self.view_seats_btn = tk.Button(self, text="查看当前航班座位", font=('Arial', 10))
        self.view_seats_btn.place(relx=0.5, rely=0.6, anchor='center')

    def update(self):
        if self.voie_text is not None and self.voie_text != "":
            result = self.get_LLM_answer(self.date, self.belonging_flight, self.user_info, self.voie_text)
            result = result.replace(" ", "").replace("[", "").replace("]", "")
            flight_id, seat_type, error_reason = result.split(",")
            print(flight_id, seat_type, error_reason)

            if flight_id != "None":
                self.user_info["flight"] = flight_id
                self.flight_label.config(text=f"当前选择航班：{flight_id}")

            if seat_type != "None":
                if flight_id != "None":
                    print(error_reason)
                else:
                    if seat_type == "window-random":
                        print("靠窗")
                        self.seat_label.config(text="当前选择座位：靠窗")
                    elif seat_type == "aisle-random":
                        print("靠走廊")
                        self.seat_label.config(text="当前选择座位：靠走廊")
                    else:
                        X, Y = seat_type.split("-")
                        print(X, Y)
                        self.seat_label.config(text=f"当前选择座位：{X}-{Y}")

            self.voie_text = None
            self.parent.start_listening()
        super().update()