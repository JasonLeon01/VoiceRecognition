import re
import tkinter as tk
from scenes.panel import Panel
from sentence_transformers import util

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

            best_match_score, best_match_instruction = self.extract_information(self.voie_text, self.sentence)

            if best_match_score < 0.15:
                print("未匹配到有效指令")
            elif "select_seat" in best_match_instruction:
                seat_info = self.extract_seat_info(self.voie_text)
                if not seat_info:
                    print("未匹配到有效的座位信息")
                else:
                    cabin, row, seat = seat_info
                    eval("self.select_seat(cabin, row, seat)")
            elif "book_meal" in best_match_instruction:
                meal_type = self.extract_meal_info(self.voie_text)
                if not meal_type:
                    print("未匹配到有效的餐食信息")
                else:
                    eval("self.book_meal(meal_type)")
            else:
                print("未匹配到有效指令")
            self.voie_text = None
            self.parent.start_listening()

        super().update()

    def extract_seat_info(self, text):
        # 使用正则表达式提取信息
        cabin_match = re.search(r"(头等舱|商务舱|经济舱)", text)
        row_match = re.search(r"([一二三四五六七八九十\d]+)排", text)
        seat_match = re.search(r"([一二三四五六七八九十\d]+)个座|([A-Z])座", text)
        
        if not (cabin_match and row_match and seat_match):
            return None  # 如果匹配失败，返回None
        
        cabin = cabin_match.group(1)  # 舱位
        row = row_match.group(1)      # 排数
        seat = seat_match.group(1)    # 座位号
        return cabin, row, seat
    
    def extract_meal_info(self, text):
        meal_match = re.search(r"(素食|牛肉|鸡肉)", text)
        if not meal_match:
            return None
        return meal_match.group(1)
    
    def select_seat(self, cabin, row, seat):
        print(f"Selecting seat: {cabin}, row {row}, seat {seat}")
        self.start_counting = True

    def book_meal(self, meal_type):
        print(f"Booking meal: {meal_type}")
        self.start_counting = True