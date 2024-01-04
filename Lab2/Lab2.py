import pandas as pd
import tkinter as tk


columns = ['ФИО', 'Паспортные данные', 'Откуда', 'Куда', 'Время отправления', 'Время прибытия', 'Номер рейса',
           'Номер вагона и места', 'Стоимость', 'Данные оплаты']

dataset = pd.read_csv('generated_dataset.csv')

    
def delete_attribute(attribute):
    dataset.drop(attribute, axis=1, inplace=True)


def locally_generalize(attribute):
    if attribute == 'ФИО':
        for i in range(len(dataset)):
            data = dataset.loc[i, attribute]
            if data[-1] == 'а':
                gender = 'Женский'
            else:
                gender = 'Мужской'
            dataset.loc[i, attribute] = gender
        dataset.rename(columns={attribute:'Пол'}, inplace=True)

    elif attribute == 'Время отправления':
        for i in range(len(dataset)):
            data = dataset.loc[i, attribute]
            month = data[data.find('-') + 1:data.rfind('-')]
            if int(month) > 11 or int(month) < 3: season = 'Зима'
            elif int(month) < 6: season = 'Весна'
            elif int(month) < 9: season = 'Лето'
            elif int(month) < 12: season = 'Осень'
            dataset.loc[i, attribute] = season
        dataset.rename(columns={attribute:'Сезон отправления'}, inplace=True)
                         
    elif attribute == 'Номер рейса':
        for i in range(len(dataset)):
            data = dataset.loc[i, attribute]
            flight_num = int(data[:-1])
            if flight_num < 299: train_type = 'Скорый'
            elif flight_num < 599: train_type = 'Пассажирский'
            elif flight_num < 751: train_type = 'Скоростной'
            else: train_type = 'Высокоскоростной'
            dataset.loc[i, attribute] = train_type
        dataset.rename(columns={attribute:'Тип поезда'}, inplace=True)
        
    elif attribute == 'Номер вагона и места':
        for i in range(len(dataset)):
            data = dataset.loc[i, attribute]
            carriage_num = data[:data.find('-')]
            if int(carriage_num) / 20 < 0.3:
                place = 'Начало'
            elif int(carriage_num) / 20 < 0.7:
                place = 'Середина'
            else:
                place = 'Конец'
            dataset.loc[i, attribute] = place
        dataset.rename(columns={attribute:'Местоположение вагона'}, inplace=True)
      
        
def micro_aggregate(attribute):
    dataset.sort_values(attribute, inplace = True)
    sum = 0
    for i in range(len(dataset)):
        data = dataset.iloc[i, dataset.columns.get_loc(attribute)]
        sum += data
        
        if i % 5000 == 0 and i > 0:
            avg = int(sum / 5000)
            for j in range (i - 5000, i):
                dataset.iloc[j, dataset.columns.get_loc(attribute)] = avg
            sum = 0
            
        if i + 1 == len(dataset):
            avg = int(sum / (5000 % len(dataset)))
            for j in range (i - (5000 % len(dataset)), i + 1):
                dataset.iloc[j, dataset.columns.get_loc(attribute)] = avg


def calculate_k():
    grouped_dataset = dataset.groupby(columns).size().reset_index(name = 'k')
    grouped_dataset.sort_values('k', inplace = True)
    k = grouped_dataset['k'].min()
    label_k.config(text=f'k-anonymity: {k}')


def calculate_k_and_grouped_dataset(attributes: list[str]):
    grouped_dataset = dataset.groupby(attributes).size().reset_index(name = 'k')
    grouped_dataset.sort_values('k', inplace = True)
    k = grouped_dataset['k'].min()
    
    bad_values = grouped_dataset[:5]
    
    k_values_count = len(grouped_dataset[grouped_dataset['k'] == k])
    
    k_values_percentage = k_values_count / len(dataset)
    
    if (k == 1):
        unique_values_count = k_values_count
    else:
        unique_values_count = 0
    
    label_k.config(text=f'k-anonymity: {k}')
    label_bad_values.insert(tk.END, bad_values)
    label_k_percentage.config(text=f'Процент записей принадлежащих k-anonymity в наборе данных: {k_values_percentage}')
    label_unique_values.config(text=f'Количество уникальных значений: {unique_values_count}')
    
    return k, grouped_dataset
    
    
def suppress_locally(needed_k: int, grouped_dataset, attributes: list[str]):
    suppressed_dataset = grouped_dataset[grouped_dataset['k'] >= needed_k]
    final_dataset = pd.DataFrame(columns=attributes)

    for _, row_to_add in suppressed_dataset.iterrows():
        repeated_rows = pd.DataFrame([row_to_add.values.tolist()[:-1]] * row_to_add['k'], columns=attributes)
        final_dataset = final_dataset._append(repeated_rows, ignore_index=True)
    
    return final_dataset


def depersonalize():
    quasi_id = []
    for flag, var in flags.items():
        if var.get():
            quasi_id.append(flag)
        
    if len(quasi_id) == 0:
        label_quasi.config(text="Выберите хотя бы 1 квази-идентификатор")
        return
    
    for attribute in columns:
        if attribute in ['Паспортные данные', 'Данные оплаты', 'Время прибытия']:
            delete_attribute(attribute)
        if attribute in ['ФИО', 'Откуда', 'Куда', 'Номер вагона и места', 'Номер рейса', 'Время отправления', 'Время прибытия']:
            locally_generalize(attribute)
        if attribute in ['Стоимость']:
            micro_aggregate(attribute)
            
    dataset.to_csv('new.txt',index=False)
            
    
        
    k, grouped_dataset = calculate_k_and_grouped_dataset(quasi_id)
        
    if len(dataset) <= 51000:
        needed_k = 10
        if k != needed_k:
            final_dataset = suppress_locally(needed_k, grouped_dataset, quasi_id)

    elif len(dataset) <= 105000:
        needed_k = 7
        if k != needed_k:
            final_dataset = suppress_locally(needed_k, grouped_dataset, quasi_id)
            
    elif len(dataset) <= 260000:
        needed_k = 5
        if k != needed_k:
            final_dataset = suppress_locally(needed_k, grouped_dataset, quasi_id)
        
    final_dataset.to_csv('depersonalized_dataset.csv', index = False)
    
            
root = tk.Tk()
root.title("Data-depersonalizator (Lab 2)")

label_quasi = tk.Label(root, text = "Выберите квази-идентификаторы")
label_quasi.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

label_k = tk.Label(root, text = "k-anonymity:")
label_k.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

label_bad_values = tk.Text(root)
label_bad_values.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

label_k_percentage = tk.Label(root, text = "Процент записей принадлежащих k-anonymity в наборе данных:")
label_k_percentage.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

label_unique_values = tk.Label(root, text = "Количество уникальных записей:")
label_unique_values.grid(row=2, column=1, padx=10, pady=10, sticky='ew')


flags = {
    "Пол": tk.BooleanVar(),
    "Откуда": tk.BooleanVar(),
    "Куда": tk.BooleanVar(),
    "Сезон отправления": tk.BooleanVar(),
    "Тип поезда": tk.BooleanVar(),
    "Местоположение вагона": tk.BooleanVar(),
    "Стоимость": tk.BooleanVar(),
}

for i, (flag, var) in enumerate(flags.items()):
    tk.Checkbutton(root, text=flag, variable=var).grid(row=i+2, column=0, pady=5, sticky='w')

depersonalize_button = tk.Button(root, text="Обезличить входной датасет", command=depersonalize)
depersonalize_button.grid(row=9, column=0, padx=10, pady=10, sticky=tk.S)

calc_quasi_button = tk.Button(root, text="Посчитать k-anonymity входного датасета", command=calculate_k)
calc_quasi_button.grid(row=9, column=1, padx=10, pady=10, sticky=tk.S)

root.mainloop()