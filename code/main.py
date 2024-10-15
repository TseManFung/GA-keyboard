# encoding: utf-8
import json,os
from random import choice
import matplotlib.pyplot as plt
import pandas as pd
import gc
from displayKeyboard import Keyboard
from matplotlib.animation import FuncAnimation
import threading
import datetime
class GA:
    def chinese_to_unicode(self,char):
        return f'{ord(char):04x}'


    def read_json(self,fileName):
        with open(rf"{fileName}", 'r', encoding='utf-8-sig') as file:
            return json.load(file)

    def check_total_distance(self,kb: Keyboard, chinese_str):
        total_distance = 0
        for char in chinese_str:
            if char in self.pattern:
                continue
            elif char == "\n":
                continue
            try:
                current_key_chanjie = choice(self.unicode2cangjie[self.chinese_to_unicode(char)])
            except:
                #print(f"Error: {char} not found in unicode2cangjie")
                continue

            for key in current_key_chanjie:
                if key == ',':
                    print(f"===\nError: {char} not found in keyboard")
                    print(f"Error: {self.chinese_to_unicode(char)} not found in keyboard")
                    print(f"Error: {current_key_chanjie} not found in keyboard\n===")
                    continue
                total_distance += kb.finger_distance(key)
        return total_distance

    def random_text(self,length:int=5000):
        text_path = r"dataset\text"
        if not os.path.exists(text_path):
            print(f"Error: {text_path} not found")
            exit()
        all_text_files = os.listdir(text_path)
        if not all_text_files:
            print(f"Error: {text_path} is empty")
            exit()
        text_file = os.path.join(text_path,choice(all_text_files))
        with open(text_file, 'r', encoding='utf-8') as file:
            text = file.readlines()
            total_lines = len(text)
            start_line = choice(range(total_lines - length))
            selected_lines = text[start_line:start_line+length]
            selected_text = ''.join(selected_lines)
        return selected_text

    def show_result(self,frame):        
        self.genetic_algorithm()
        result = pd.DataFrame({'Fastest': self.Fastest, 'Average': self.Average, 'Control': self.Control})
        
        plt.cla()
        line1, = plt.plot(result.index, result.Fastest, label=f'Fastest: {self.Fastest[-1] if self.Fastest else "no data"}', color='red')
        line2, = plt.plot(result.index, result.Average, label=f'Average: {self.Average[-1] if self.Average else "no data"}', color='blue')
        line3, = plt.plot(result.index, result.Control, label=f'Control: {self.Control[-1] if self.Control else "no data"}', color='black')
        
        plt.xlabel('Number of iterations')
        plt.gca().get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:d}".format(int(x))))
        plt.ylabel('Total distance')
        plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        plt.title(f'Fastest Keyboard: {self.Top_keyboard[0]}', loc='left')
        plt.legend(loc='lower left')
        
        return line1, line2, line3

    # GA
    def Top4(self,population: list[Keyboard], chinese_str:str):
        for kb in population:
            kb.Total_Distance = self.check_total_distance(kb, chinese_str)
        population.sort(key=lambda x: x.Total_Distance)
        self.Fastest.append(population[0].Total_Distance)
        self.Average.append(sum([kb.Total_Distance for kb in population])/len(population))
        self.Control.append(self.check_total_distance(self.control_kb, chinese_str))
        return population[:4]

    def crossover(self,population_size:int,Top_keyboard: list[Keyboard]):
        next_gen = []
        DNA_list = [] #[[{}*8],[{}*8],[{}*8],[{}*8]]
        for kb in Top_keyboard:
            DNA_list.append(kb.get_finger_key_group())
        DNA_fragment_length = len(DNA_list[0])
        for i in range(population_size):
            DNA_fragment = []
            for fragment_index in range(DNA_fragment_length):
                DNA_fragment.append(choice(DNA_list)[fragment_index])
            next_gen.append(Keyboard(keyboard=Keyboard.set_new_keyboard(DNA_fragment)))
        return next_gen

    def init_population(self,starting_population:int=4):
        kb_pop =[]
        kb = Keyboard()
        kb_pop.append(kb)
        key_list = list(kb.keyboard.keys())
        for i in range(starting_population-1):
            kb_pop.append(Keyboard())
            for _ in range(1000):
                kb_pop[-1].swap(choice(key_list), choice(key_list))
        return kb_pop
            

    def genetic_algorithm(self):
        if self.generations == 1:
            print(f"Fastest: {self.Fastest[-1]}\nKeyboard: {self.Top_keyboard[0]}")
            t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            if not os.path.exists(rf'result/{t}'):
                os.makedirs(rf'result/{t}')
            self.Top_keyboard[0].save("keyboard",t)
            self.fig.savefig(rf'result/{t}/chart_{t}.png')
            self.generations = 0
            return
        if self.generations == 0:
            return
        if not self.Fastest:
            population = self.init_population()
            self.Top_keyboard = self.Top4(population, self.random_text())
        population = self.crossover(self.population_size,self.Top_keyboard)
        self.Top_keyboard = self.Top4(population, self.random_text())
        gc.collect()
        self.generations -= 1

    def __init__(self,population_size:int=None,generations:int=None):
        if not population_size:
            population_size = 256
        else:
            self.population_size = population_size
        if not generations:
            generations = 1000
        else:
            self.generations = generations

    def main(self):
        self.unicode2cangjie = self.read_json(r"dataset\cangjie\unicode2cangjie.json")
        self.pattern = r'[\t ，。,.:：;；!！?？—\-「」『』【】《》〈〉〔〕〖〗〘〙〚〛〝〞〟〰‥…‧﹏﹑﹔﹖﹪﹫？｡。\\/:*?"<>|\(\)─（）／＊、]★'

        self.Fastest = []
        self.Average = []
        self.Control = []
        self.control_kb = Keyboard()
        self.Top_keyboard = [self.control_kb]
        self.fig, ax = plt.subplots()
        ani = FuncAnimation(self.fig, self.show_result, frames=100, interval=200, blit=False) 
        plt.show()
        
    
if __name__ == "__main__":
    t1 = threading.Thread(target=GA().main)
    t1.start()
