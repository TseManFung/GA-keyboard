# encoding: utf-8
import json,os
from random import choice, shuffle
import matplotlib.pyplot as plt
import pandas as pd
import threading
from copy import copy
from displaykeyboard import Keyboard


pattern = r'[\t ，。,.:：;；!！?？—\-「」『』【】《》〈〉〔〕〖〗〘〙〚〛〝〞〟〰‥…‧﹏﹑﹔﹖﹪﹫？｡。\\/:*?"<>|\(\)─（）／＊、]★'

def chinese_to_unicode(char):
    return f'{ord(char):04x}'


def read_json(fileName):
    with open(rf"{fileName}", 'r', encoding='utf-8-sig') as file:
        return json.load(file)


""" def check_total_distance(chinese_str):
    global last_changjie
    total_distance = 0
    for char in chinese_str:
        if char in pattern:
            continue
        elif char == "\n":
            last_changjie = ""
            continue
        try:
            current_key_chanjie = last_changjie + choice(
                unicode2cangjie[chinese_to_unicode(char)])
        except:
            print(f"Error: {char} not found in unicode2cangjie")
            continue
        len_current_key = len(current_key_chanjie)
        for key in range(min(1, len_current_key - 1), len_current_key):
            total_distance += displaykeyboard.distance(
                displaykeyboard.keyboard, current_key_chanjie[key - 1],
                current_key_chanjie[key])
        last_changjie = current_key_chanjie[-1]
    return total_distance """


def check_total_distance(kb: Keyboard, chinese_str):
    total_distance = 0
    for char in chinese_str:
        if char in pattern:
            continue
        elif char == "\n":
            continue
        try:
            current_key_chanjie = choice(unicode2cangjie[chinese_to_unicode(char)])
        except:
            #print(f"Error: {char} not found in unicode2cangjie")
            continue

        for key in current_key_chanjie:
            total_distance += kb.finger_distance(key)
    return total_distance

def random_text(length:int=5000):
    text_path = r"dataset\text"
    all_text_files = os.listdir(text_path)
    text_file = os.path.join(text_path,choice(all_text_files))
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.readlines()
        total_lines = len(text)
        start_line = choice(range(total_lines - length))
        selected_lines = text[start_line:start_line+length]
        selected_text = ''.join(selected_lines)
    return selected_text


def show_result(Fastest, Average, Control):
    result = pd.DataFrame({'Fastest':Fastest, 'Average':Average, 'Control':Control})
    
    plt.plot(result.index,result.Fastest, label='Fastest', color='red')
    plt.plot(result.index,result.Average, label='Average', color='blue')
    plt.plot(result.index,result.Control, label='Control', color='black')
    plt.xlabel('Number of iterations')
    plt.ylabel('Total distance')
    plt.title('Total distance of different keyboard layouts')
    plt.legend(loc='lower left')
    plt.show()

# GA
def genetic_algorithm(population_size:int=256, generations:int=1000):
    control_kb = Keyboard()

def crossover():
    pass

def init_population(starting_population:int=4):
    kb_pop =[]
    kb = Keyboard()
    kb_pop.append(kb)
    key_list = list(kb.keyboard.keys())
    for i in range(starting_population-1):
        kb_pop.append(Keyboard())
        for _ in range(1000):
            kb_pop[-1].swap(choice(key_list), choice(key_list))
    return kb_pop
        

def test():
    global unicode2cangjie
    unicode2cangjie = read_json(r"dataset\cangjie\unicode2cangjie.json")
    chinese_str = random_text()
    kb_pop = init_population()
    for kb in kb_pop:
        print(kb)
        print(f"Total distance: {check_total_distance(kb, chinese_str)}")


def main():
    test()
    
if __name__ == "__main__":
    main()
