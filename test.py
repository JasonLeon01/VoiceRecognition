import LLM

date = "2025-02-04"

belonging_flight = {
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

flight_seat = {
  "Air-Beijing-Shanghai-2025-03-05-10-25-00": {
    "first": [
      [True, False],
      [False, False]
    ],
    "business": [
      [True, False, False, False]
    ],
    "economy": [
      [False, False, False, True, False, True]
    ]
  }
}

user_info = {
  "flight": "None",
  "seat": ["None", -1, -1]
}

dialogue = "我要三月份那趟航班的走廊的座位"

print(LLM.LLM.get_info(date, belonging_flight, flight_seat, user_info, dialogue))