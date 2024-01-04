import tkinter as tk
from tkinter import Label, Entry, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import numpy as np
import time

def f(x1, x2): # функция, минимум которой необходимо найти
    return 8 * (x1 * x1) + 4 * x1 * x2 + 5 * (x2 * x2)

class Particle:
    def __init__(self, numdim, numpart, inertia, perscf, globalcf, vel, pos):
        self.numpart = numpart
        self.inertia = inertia
        self.perscf = perscf
        self.globalcf = globalcf
        self.velocity = vel
        self.position = pos
        self.part = [self.create(numdim) for _ in range(numpart)]
        
    # создание индивидуальной частицы с начальным положением и скоростью
    def create(self, numdim):
        posit = np.array([random.uniform(0-self.position, self.position) for _ in range(numdim)])
        velos = np.array([random.uniform(0-self.velocity, self.velocity) for _ in range(numdim)])
        return {'pos': posit, 'vel': velos, 'bpos': np.copy(posit), 'bval': float('inf')}
    
    # обновление положения и скорости частицы
    def update(self, p, gbpos, iteration, max_iter):
        # вычисление инерции с учетом текущей итерации
        ci = self.inertia * (1 - iteration / max_iter)
        # вычисление компонентов для обновления скорости
        it = ci * p['vel']
        pt = self.perscf * random.random() * (p['bpos'] - p['pos'])
        gt = self.globalcf * random.random() * (gbpos - p['pos'])
        # обновление скорости и положения
        p['vel'] = it + pt + gt
        p['pos'] += p['vel']
        # оценка значения функции в новом положении
        cv = f(p['pos'][0], p['pos'][1])

        #обновление лучшего положения, если значение функции уменьшилось
        if cv < p['bval']:
            p['bval'] = cv
            p['bpos'] = np.copy(p['pos'])

def init():
    # считывание входных данных
    npart = int(root.npe.get())
    inertia = float(root.ie.get())
    perscf = float(root.pe.get())
    globalcf = float(root.ge.get())
    num_iter = int(root.itere.get())
    vel = int(root.vele.get())
    pos = int(root.pose.get())

    root.result_label.config(text='') # очистка поля
    
    frst_time = time.time()
    
    swarm = Particle(2, npart, inertia, perscf, globalcf, vel, pos)
    gbpos = np.zeros(2)
    gbval = float('inf')
    
    # итерации для поиска минимума
    for i in range(num_iter):
        for p in swarm.part:
            # обновление каждой частицы в рое
            swarm.update(p, gbpos, i, num_iter)
            cv = f(p['pos'][0], p['pos'][1])

        # обновление глобального лучшего значения и положения
            if cv < gbval:
                gbval = cv
                gbpos = np.copy(p['pos'])
                
        # отображение результата
    root.ax.clear() 
    poss = np.array([p['pos'] for p in swarm.part])
    root.ax.scatter(poss[:, 0], poss[:, 1], label='Результат')
    root.ax.legend()
    root.canvas.draw()

    root.result_label.config(text=f'Найденная точка: {gbpos}\nЗначение функции в найденной точке: {gbval}')
    
    scnd_time = time.time()
    print(scnd_time - frst_time)

root = tk.Tk()
root.title('Swarm Algorithm (Lab 5)')

Label(root, text='Максимальный модуль начальной скорости:').pack()
root.vele = Entry(root)
root.vele.pack()

Label(root, text='Максимальный модуль начального положения:').pack()
root.pose = Entry(root)
root.pose.pack()

Label(root, text='Количество частиц:').pack()
root.npe = Entry(root)
root.npe.pack()

Label(root, text='Коэффициент инерции:').pack()
root.ie = Entry(root)
root.ie.pack()

Label(root, text='Коэффициент персонального опыта:').pack()
root.pe = Entry(root)
root.pe.pack()

Label(root, text='Коэффициент общего опыта:').pack()
root.ge = Entry(root)
root.ge.pack()

Label(root, text='Количество итераций:').pack()
root.itere = Entry(root)
root.itere.pack()

Button(root, text='Найти минимум', command=init).pack()

root.result_label = Label(root, text='')
root.result_label.pack()

root.fig, root.ax = plt.subplots()
root.canvas = FigureCanvasTkAgg(root.fig, master=root)
root.canvas_widget = root.canvas.get_tk_widget()
root.canvas_widget.pack()

root.mainloop()