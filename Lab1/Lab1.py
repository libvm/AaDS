import pandas as pd
import random
import tkinter as tk
import json
from enum import Enum
from datetime import datetime, timedelta

class Cities(Enum):
    Архангельск = 0
    Новгород = 1
    Владивосток = 2
    Екатеринбург = 3
    Казань = 4
    Москва = 5
    Новосибирск = 6
    Ростов = 7
    СанктПетербург = 8
    Сочи = 9
    УланУдэ = 10
    Уфа = 11
    
class Banks(Enum):
    Сбербанк = 0
    Тинькофф = 1
    Уралсиб = 2
    АльфаБанк = 3
    
class Systems(Enum):
    МИР = 0
    MasterCard = 1
    default = 2

def generate_passport_data(n: int):
    all_passport_data = set()
    while len(all_passport_data) < n:
        all_passport_data.add(f'{random.randint(1000, 9999)} {random.randint(100000, 999999)}')
    return all_passport_data


banks = [str(i).replace("\n", "") for i in open('banks.txt', encoding = 'utf-8').readlines()]
payment_systems = [str(i).replace("\n", "") for i in open('payment_systems.txt', encoding = 'utf-8').readlines()]
bins = json.load(open('binBanks.json'))

def generate_card_numbers(banks_percentages: list[float], sys_percentages: list[float], n: int):
    card_numbers = dict()
    while len(card_numbers) < n:
        bank = random.choices(banks, weights = banks_percentages, k = 1)[0]
        payment_system = random.choices(payment_systems, weights = sys_percentages, k = 1)[0]
        card_number = f'{bins[Systems[payment_system].value][Banks[bank].value]} {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}'
        card_numbers_keys = card_numbers.keys()
        if card_number in card_numbers_keys:
            if card_numbers[card_number] > 5:
                continue
            card_numbers[card_numbers] += 1
        else:
            card_numbers[card_number] = 1
    return card_numbers


carriages_and_costs = json.load(open('carriages_and_costs.json'))    

def generate_carriage():
    train = random.choice(carriages_and_costs)
    carriage_type = random.choice(train['carriageType'])
    carriage = random.choice(carriage_type['carriages'])
    return carriage, carriage_type['baseCost'], carriage_type['seatCount']


cities = [str(i).replace("\n", "") for i in open('cities.txt', encoding = 'utf-8').readlines()]

def generate_departure_and_destination():
    departure = random.choice(cities)
    destination = random.choice(cities)
    while departure == destination:
        destination = random.choice(cities)
    return departure, destination


male_first_names = [str(i).replace("\n", "") for i in open('male_firstnames.txt', encoding = 'utf-8').readlines()]
male_last_names = [str(i).replace("\n", "") for i in open('male_lastnames.txt', encoding = 'utf-8').readlines()]
male_surnames = [str(i).replace("\n", "") for i in open('male_surnames.txt', encoding = 'utf-8').readlines()]
female_first_names = [str(i).replace("\n", "") for i in open('female_firstnames.txt', encoding = 'utf-8').readlines()]
female_last_names = [str(i).replace("\n", "") for i in open('female_lastnames.txt', encoding = 'utf-8').readlines()]
female_surnames = [str(i).replace("\n", "") for i in open('female_surnames.txt', encoding = 'utf-8').readlines()]

def generate_name():
    if random.choice([0, 1]):
        return random.choice(male_first_names) + " " + random.choice(male_last_names) + " " + random.choice(male_surnames)
    else: 
        return random.choice(female_first_names) + " " + random.choice(female_last_names) + " " + random.choice(female_surnames)
    
def generate_flight_number():
    flight_type = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    return int(f'{random.randint(1, 7)}{random.randint(1, 88)}'), flight_type


distances = json.load(open('distances.json'))

def generate_cost(base_cost: int, distance: int, flight_number: int):
    if flight_number < 151:
        cost = base_cost * (distance / 2000) * 1.2
    elif flight_number < 299:
        cost = base_cost * (distance / 2000) * 1.3
    elif flight_number < 451:
        cost = base_cost * (distance / 2000) * 1
    elif flight_number < 599:
        cost = base_cost * (distance / 2000) * 1.1
    elif flight_number < 751:
        cost = base_cost * (distance / 2000) * 1.4
    else:
        cost = base_cost * (distance / 2000) * 1.5
    return int(cost)

def generate_dates(distance: int, flight_number: int):
    current_datetime = datetime.now()

    random_days = random.randint(0, 365)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)

    departure_date = current_datetime - timedelta(days = random_days,
                                                    hours = random_hours,
                                                    minutes = random_minutes,
                                                    seconds = random_seconds)
    
    if flight_number < 151:
        hours = distance / 60
    elif flight_number < 299:
        hours = distance / 70
    elif flight_number < 451:
        hours = distance / 40
    elif flight_number < 599:
        hours = distance / 50
    elif flight_number < 751:
        hours = distance / 91 
    else:
        hours = distance / 161
    hours = int(distance) / 65
    arrival_date = departure_date + timedelta(hours = hours)
    return departure_date.strftime("%Y-%m-%d %H:%M:%S"), arrival_date.strftime("%Y-%m-%d %H:%M:%S")        
       
def generate_dependent_data(n: int):
    dependent_data = set()
    while len(dependent_data) < n:
        carriage, base_cost, max_seat_count = generate_carriage()
        seat = random.randint(1, max_seat_count)
        departure, destination = generate_departure_and_destination()
        full_name = generate_name()
        flight_number, flight_letter = generate_flight_number()
        distance = distances[Cities[departure].value][Cities[destination].value] 
        cost = generate_cost(base_cost, distance, flight_number)
        departure_date, arrival_date = generate_dates(distance, flight_number)
        dependent_data.add((full_name, departure_date, arrival_date, f'{flight_number}{flight_letter}', f'{carriage}-{seat}', cost, departure, destination))
    return dependent_data

 
records = 50000

def generate_and_write_data(banks_percentages: list[float], sys_percentages: list[float]):
    card_numbers = generate_card_numbers(banks_percentages, sys_percentages, records)
    card_numbers = list(card_numbers.keys())
    all_passport_data = generate_passport_data(records)
    all_passport_data = list(all_passport_data)
    dependent_data = generate_dependent_data(records)
    dependent_data = list(dependent_data)
    
    columns = ['ФИО', 'Паспортные данные', 'Откуда', 'Куда', 'Время отправления', 'Время прибытия', 'Номер рейса',
           'Номер вагона и места', 'Стоимость', 'Данные оплаты']
    dataset = pd.DataFrame(columns = columns)
    
    for i in range(records):
        passport_data = all_passport_data[i]
        full_name, departure_date, arrival_date, flight_number, carriage_and_seat, cost, departure, destination = dependent_data[i]
        card_number = card_numbers[i]
        data = [full_name, passport_data, departure, destination, departure_date, arrival_date,
            flight_number, carriage_and_seat, cost, card_number]
        dataset = dataset._append(pd.Series(data, index=columns), ignore_index=True)    
    dataset.to_csv('generated_dataset.csv', index=False)

def on_button_click():
    banks_percentages = [float(num) / 100 for num in entry_banks.get().split()]
    sys_percentages = [float(num) / 100 for num in entry_systems.get().split()]
    if sum(banks_percentages) != 1.0 or sum(sys_percentages) != 1.0 or len(banks_percentages) != len(banks) or len(sys_percentages) != len(payment_systems):
        message.config(text = "Введены неверные значения коэффициентов")
    else:
        message.config(text = "Генерация...")
        root.after(100)
        root.update_idletasks()
        generate_and_write_data(banks_percentages, sys_percentages)
        message.config(text = "Генерация завершена")
    
root = tk.Tk()
root.title("Dataset generator (lab 1)")

label_banks = tk.Label(root, text = "Введите проценты вероятностей через пробел на генерацию банков:\n 1. Сбербанк \n 2. Тинькофф \n 3. Уралсиб \n 4. АльфаБанк")
label_banks.pack(pady = 5)

entry_banks = tk.Entry(root)
entry_banks.pack(pady = 5)

label_systems = tk.Label(root, text = "Введите проценты вероятностей через пробел на генерацию платежных систем: \n 1. МИР \n 2. MasterCard \n 3. default")
label_systems.pack(pady = 5)

entry_systems = tk.Entry(root)
entry_systems.pack(pady = 5)

button = tk.Button(root, text = "Сгенерировать датасет", command=on_button_click)
button.pack(pady = 10)

message = tk.Label(root)
message.pack(pady = 5)
root.mainloop()