# encoding: utf-8
import json
import os
from random import choice
import matplotlib.pyplot as plt
from numpy import sqrt
import pandas as pd
import gc
from displaykeyboard import Keyboard
from matplotlib.animation import FuncAnimation
import datetime
from tqdm import tqdm
import multiprocessing as mp
from threading import Thread


class GA:

    def chinese_to_unicode(self, char):
        return f'{ord(char):04x}'

    def read_json(self, fileName):
        with open(rf"{fileName}", 'r', encoding='utf-8-sig') as file:
            return json.load(file)

    def check_total_distance(self, kb: Keyboard, chinese_str):
        total_distance = 0
        for char in chinese_str:
            if char in self.pattern:
                continue
            elif char == "\n":
                continue
            try:
                current_key_chanjie = choice(self.unicode2cangjie[
                    self.chinese_to_unicode(char)][0].split(','))
            except:
                # print(f"Error: {char} not found in unicode2cangjie")
                continue

            for key in current_key_chanjie:
                total_distance += kb.finger_distance(key)
        return total_distance

    def random_text(self, length: int = 5000):
        text_path = r"dataset\text"
        if not os.path.exists(text_path):
            print(f"Error: {text_path} not found, it will be auto created")
            os.makedirs(text_path)
        all_text_files = os.listdir(text_path)
        if not all_text_files:
            print(f"Error: {text_path} is empty")
            os.system(rf'start {os.path.abspath(text_path)}')
            exit()
        text_file = os.path.join(text_path, choice(all_text_files))
        with open(text_file, 'r', encoding='utf-8') as file:
            text = file.readlines()
            total_lines = len(text)
            start_line = choice(range(total_lines - length))
            selected_lines = text[start_line:start_line + length]
            selected_text = ''.join(selected_lines)
        return selected_text

    # GA
    def find_top_keyboard(self, population: list[Keyboard], chinese_str: str):
        population.append(self.tk)
        with mp.Pool(self.cpu_count) as pool:
            distance_result = pool.starmap(self.check_total_distance,
                                           [(kb, chinese_str)
                                            for kb in population])
        for i in range(len(population)):
            population[i].Total_Distance = distance_result[i]
        population.sort(key=lambda x: x.Total_Distance)
        self.tk = population[0]
        self.Fastest.append(self.tk.Total_Distance)
        self.Average.append(
            sum([kb.Total_Distance for kb in population]) / len(population))
        self.Control.append(
            self.check_total_distance(self.control_kb, chinese_str))
        parent_size = sqrt(self.population_size)
        random_size = int(parent_size * self.mutation_rate)
        print(f"{parent_size=}, {random_size=}")
        self.Top_keyboard = population[:int(parent_size) -
                                       random_size] + self.random_keyboard(
                                           random_size)

    def crossover(self, population_size: int, Top_keyboard: list[Keyboard]):
        next_gen = []
        DNA_list = []  # [[{}*8],[{}*8],[{}*8],[{}*8]]
        for kb in Top_keyboard:
            DNA_list.append(kb.get_finger_key_group())
        DNA_fragment_length = len(DNA_list[0])
        for i in range(population_size):
            DNA_fragment = []
            for fragment_index in range(DNA_fragment_length):
                DNA_fragment.append(choice(DNA_list)[fragment_index])
            next_gen.append(
                Keyboard(keyboard=Keyboard.set_new_keyboard(DNA_fragment)))
        return next_gen

    def init_population(self, starting_population: int = 4):
        kb_pop = []
        kb = Keyboard()
        kb_pop.append(kb)
        self.key_list = list(kb.keyboard.keys())
        kb_pop += self.random_keyboard(starting_population - 1)
        return kb_pop

    def random_keyboard(self, n: int):
        kb_pop = []
        for i in range(n):
            kb_pop.append(Keyboard())
            for _ in range(1000):
                kb_pop[-1].swap(choice(self.key_list), choice(self.key_list))
        return kb_pop

    def genetic_algorithm(self):
        if not self.Fastest:
            population = self.init_population()
            self.find_top_keyboard(population,
                                   self.random_text(self.text_length))
        for _ in tqdm(range(self.generations), desc='Generations'):
            population = self.crossover(self.population_size,
                                        self.Top_keyboard)
            self.find_top_keyboard(population,
                                   self.random_text(self.text_length))
            self.df = pd.DataFrame({
                'Fastest': self.Fastest,
                'Average': self.Average,
                'Control': self.Control
            })
            gc.collect()
        print(f"Fastest: {self.Fastest[-1]}\nKeyboard: {self.Top_keyboard[0]}")
        t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if not os.path.exists(rf'result/{t}'):
            os.makedirs(rf'result/{t}')
        self.Top_keyboard[0].save("keyboard", t)
        try:
            self.fig.savefig(rf'result/{t}/chart_{t}.png')
        except:
            pass

    def __init__(self,
                 population_size: int = 256,
                 generations: int = 1000,
                 text_length: int = 5000,
                 mutation_rate: float = 0.2):
        self.population_size = population_size
        self.generations = generations
        self.text_length = text_length
        self.mutation_rate = mutation_rate

        self.pattern = r'[\t ，。,，.:：;；!！?？—\-「」『』【】《》〈〉〔〕〖〗〘〙〚〛〝〞〟〰‥…‧﹏﹑﹔﹖﹪﹫？｡。\\/:*?"<>|\(\)─（）／＊、]★'
        self.Fastest = []
        self.Average = []
        self.Control = []
        self.tk = self.control_kb = Keyboard()
        self.Top_keyboard = [self.control_kb]
        self.df = pd.DataFrame({
            'Fastest': self.Fastest,
            'Average': self.Average,
            'Control': self.Control
        })

    def init_func(self):
        # plt.ion()
        plt.xlabel('Number of iterations')
        plt.ylabel('distance increase rate (%)')
        

    def format_x_axis(self, x, loc):
        return "{:d}".format(int(x))

    def format_y_axis(self, x, loc):
        return "{:d}".format(int(x*100))

    def show_result(self, f):
        result = self.df
        plt.cla()
        self.init_func()
        plt.gca().get_xaxis().set_major_formatter(
            plt.FuncFormatter(self.format_x_axis))
        plt.gca().get_yaxis().set_major_formatter(
            plt.FuncFormatter(self.format_y_axis))
        plt.title(f'Fastest Keyboard: {self.tk}', loc='left')
        plt.plot(
            result.index,
            (result.Control-result.Fastest)/result.Control,
            label=f'Fastest: {self.Fastest[-1]
                              if self.Fastest else "no data"}',
            color='red')
        plt.plot(
            result.index,
            (result.Control-result.Average)/result.Control,
            label=f'Average: {self.Average[-1]
                              if self.Average else "no data"}',
            color='blue')
        plt.plot(
            result.index,
            result.Control-result.Control,
            label=f'Control: {self.Control[-1]
                              if self.Control else "no data"}',
            color='black')
        plt.legend(loc='lower left')

    def main(self,join=False):
        self.unicode2cangjie = self.read_json(
            r"dataset\cangjie\unicode2cangjie.json")
        self.fig = fig
        self.init_func()
        ga_thread = Thread(target=self.genetic_algorithm)
        ga_thread.start()
        if join:
            ga_thread.join()

    def set_cpu_core(self, count: int = mp.cpu_count()):
        self.cpu_count = count


def To_int(x):
    try:
        return int(x)
    except:
        return -1


def To_float(x):
    try:
        return float(x)
    except:
        return -1


if __name__ == "__main__":

    population_size = To_int(
        input("Enter the population size(default = 256), must >=40: "))
    if population_size < 40:
        print("The population size set to default 256")
        population_size = 256

    generations = To_int(
        input("Enter the number of generations(default = 1000), must >=1: "))
    if generations < 1:
        print("The number of generations set to default 1000")
        generations = 1000

    text_length = To_int(
        input("Enter the length of the text(default = 5000), must >=100: "))
    if text_length < 100:
        print("The length of the text set to default 5000")
        text_length = 5000
    min_mutation_rate = 1/sqrt(population_size)
    mutation_rate = To_float(
        input(
            f"Enter the mutation rate(suggest to use default = {min_mutation_rate}), must between 0 and 1: "))
    if mutation_rate < 0 or mutation_rate > 1:
        print(f"The mutation rate set to default {min_mutation_rate}")
        mutation_rate = 0.2
    max_cpu_core = mp.cpu_count()-1
    cpu_core = To_int(
        input(
            f"Enter the number of CPU cores(default = {max_cpu_core}), must between 1 and {
                max_cpu_core}: "
        ))
    if cpu_core < 1 or cpu_core > max_cpu_core:
        print(f"The number of CPU cores set to default {max_cpu_core}")
        cpu_core = max_cpu_core
    animate_chart = input("Do you want to animate the chart?(y/n) (default y): ")


    ga = GA(population_size=population_size,
            generations=generations,
            text_length=text_length,
            mutation_rate=mutation_rate)
    ga.set_cpu_core(count=cpu_core)
    fig, ax = plt.subplots()
    try:
        if animate_chart.lower() == 'n':
            ga.main(join=True)
            ga.show_result(fig)
        else:
            ani = FuncAnimation(fig, ga.show_result, init_func=ga.main,
                                cache_frame_data=False, repeat=False)
        fig.set_size_inches(8, 8)
        plt.show()
        if animate_chart.lower() == 'n':
            t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            if not os.path.exists(rf'result/{t}'):
                os.makedirs(rf'result/{t}')
            fig.savefig(rf'result/{t}/chart_{t}.png')
    except KeyboardInterrupt:
        if animate_chart.lower() == 'n':
            t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            if not os.path.exists(rf'result/{t}'):
                os.makedirs(rf'result/{t}')
            ga.Top_keyboard[0].save("keyboard", t)
            fig.savefig(rf'result/{t}/chart_{t}.png')
        plt.show()
        
