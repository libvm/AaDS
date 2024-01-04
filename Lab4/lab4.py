import tkinter as tk
from tkinter import ttk
import numpy as np
import time

def f(x1, x2): # функция, минимум которой необходимо вычислить
    return 8 * (x1 * x1) + 4 * x1 * x2 + 5 * (x2 * x2)

class Genetic:
    def __init__(self, mutate_chance, chromo_num, genes_min, genes_max, generations_num, encoding_type):
        self.mutate_chance = mutate_chance / 100.0
        self.chromo_num = chromo_num
        self.genes_min = genes_min
        self.genes_max = genes_max
        self.generations_num = generations_num
        self.population = set()
        self.encoding_type = encoding_type
        self.generate_population()
        
    def run(self): # запуск генетического алгоритма
        for _ in range(self.generations_num):
            self.mutate()
            self.crossover()
            self.select()
        
    def generate_population(self): # генерация начальной популяции
        self.population = set()

        for _ in range(self.chromo_num):
            # генерация пары генов для каждой хромосомы
            gene1, gene2 = self.generate_gene_pair()

            # вычисление значения функции приспособленности для каждой хромосомы
            result = f(gene1, gene2)

            # добавление кортежа с генами и значением функции приспособленности в популяцию
            self.population.add((result, gene1, gene2))

    def generate_gene_pair(self): # генерация пары генов в зависимости от типа кодирования
        if self.encoding_type == 'Бинарная':
            gene1_binary = format(np.random.randint(int(self.genes_min), int(self.genes_max)), 'b')
            # генерация случайных бинарных строк
            gene2_binary = format(np.random.randint(int(self.genes_min), int(self.genes_max)), 'b')
            # преобразуем бинарные строки в целые числа
            gene1, gene2 = int(gene1_binary, 2), int(gene2_binary, 2)
            
        elif self.encoding_type == 'Вещественная':
            #генерирация случайных вещественных числа
            gene1, gene2 = np.random.uniform(self.genes_min, self.genes_max), np.random.uniform(self.genes_min, self.genes_max)

        return gene1, gene2


    def select(self): # выбор лучших хромосом для следующего поколения
        self.population = sorted(self.population, key=lambda x: x[0])[:self.chromo_num]

    def crossover(self): # cоздание нового поколения из пар предков
        new_population = set()

        # проход по парам предков
        for i in range(0, self.chromo_num, 2):
            parent1, parent2 = np.array(self.population[i]), np.array(self.population[i + 1])

            # генерация случайных весов для скрещивания
            alpha = np.random.rand(2)

            # скрещивание для создания двух потомков
            child1 = alpha * parent1 + (1 - alpha) * parent2
            child2 = alpha * parent2 + (1 - alpha) * parent1

            # добавление потомков в новую популяцию с вычислением их функции приспособленности
            for child in (child1, child2):
                new_population.add(child[0], child[1], f[child[0], child[1]])

        # замена старой популяции на новую
        self.population = new_population


    def mutate(self): # изменение генов некоторых хромосом
        for i in range(self.chromo_num):
            # проверка на то, произойдет ли мутация с вероятностью mutate_chance
            if np.random.random() < self.mutate_chance:
                parent = np.array(self.population[i])
                
                # генерация случайного смещения
                mutate_shift = np.random.normal(0, 2)
                
                # добавление к предку смещения для получения нового потомка
                child = parent + mutate_shift
                
                # вычисление значения функции приспособленности для мутировавшей хромосомы
                child_result = f(child[0], child[1])
                
                # замена исходной хромосомы на мутировавшую
                self.population[i] = (child_result, child[0], child[1])


    def get_best_result(self): # получение лучшего решения в текущей популяции
        get_best_result = min(self.population, key=lambda x: x[0])
        return get_best_result[0], get_best_result[1], get_best_result[2]
    
    def get_population(self): # получение информации о популяции
        result = set()

        for i, chromosome in enumerate(self.population):
            updated_chromosome = (i + 1, chromosome[0], chromosome[1], chromosome[2])
            result.add(updated_chromosome)

        return result


def init():
    # получение параметров из пользовательского ввода
    frst_time = time.time()
    if root.mutate_prob.get() == '' or root.chromo_num.get() == '' \
    or root.genes_min.get() == '' or root.genes_max.get() == '' \
        or root.generations_num.get() == '' or root.encoding_box.get() == '':
            prob_l.config(text='Укажите все значения!')
            pass
    else:
        prob_l.config(text='Вероятность мутации(от 0 до 100):')


    mutate_chance = float(root.mutate_prob.get())
    if mutate_chance < 0 or mutate_chance > 100:
        prob_l.config(text='Вероятность должна быть в пределах от 0 до 100!')
        pass

    
    chromo_num = int(root.chromo_num.get())
    genes_min = float(root.genes_min.get())
    genes_max = float(root.genes_max.get())
    generatations_num = int(root.generations_num.get())
    encoding_type = root.encoding_box.get()
    

    genetic_algorithm = Genetic(mutate_chance, chromo_num, genes_min, genes_max, generatations_num, encoding_type)
    
    get_best_result = genetic_algorithm.get_best_result()
    population_data = genetic_algorithm.get_population()

    root.result_text.delete(1.0, tk.END)
    root.result_text.insert(tk.END, f'Найденная точка:\nx1={get_best_result[0]}\nx2={get_best_result[1]}\n')
    root.result_text.insert(tk.END, f'Значение функции в точке:\n{get_best_result[2]}')
    
    
    
    root.table_text.delete(1.0, tk.END)
    for result in population_data:
        root.table_text.insert(tk.END, f"{result[0]}: Результат={result[1]}, 1 ген={result[2]}, 2 ген={result[3]}\n")
        
    scnd_time = time.time()
    print(scnd_time-frst_time)

root = tk.Tk()
root.title('Genetic algorythm (lab 4)')
prob_l = tk.Label(root, text='Вероятность мутации(от 0 до 100):')
prob_l.pack()
root.mutate_prob = tk.Entry(root)
root.mutate_prob.pack()

tk.Label(root, text='Количество хромосом:').pack()
root.chromo_num = tk.Entry(root)
root.chromo_num.pack()

tk.Label(root, text='Мин. значение гена:').pack()
root.genes_min = tk.Entry(root)
root.genes_min.pack()

tk.Label(root, text='Макс. значение гена:').pack()
root.genes_max = tk.Entry(root)
root.genes_max.pack()

tk.Label(root, text='Количество итераций:').pack()
root.generations_num = tk.Entry(root)
root.generations_num.pack()

tk.Label(root, text='Тип кодировки:').pack()
root.encoding_box = ttk.Combobox(root, values=['Бинарная', 'Вещественная'])
root.encoding_box.pack()

tk.Button(root, text='Найти минимум', command=init).pack()

root.result_text = tk.Text(root, height=5, width=50)
root.result_text.pack()

tk.Label(root, text='Хромосомы:').pack()
root.table_text = tk.Text(root, height=10, width=50)
root.table_text.pack()

root.mainloop()