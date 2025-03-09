import random

def generate_seat_availability(rows, seats_per_row):
    return [[random.choice([True, False]) for _ in range(seats_per_row)] for _ in range(rows)]

# 头等舱
first_class = {
    'first': generate_seat_availability(4, 2)
}

# 商务舱
business_class = {
    'business': generate_seat_availability(8, 4)
}

# 经济舱
economy_class = {
    'economy': generate_seat_availability(30, 6)
}

# 合并所有舱室数据
seat_availability = {**first_class, **business_class, **economy_class}

# 打印结果
for cabin, seats in seat_availability.items():
    print(f"{cabin} class seat availability:")
    for row in seats:
        print(row)
    print()