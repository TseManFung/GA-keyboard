# encoding: utf-8
import json,os
from random import choice
import matplotlib.pyplot as plt
import pandas as pd
import threading
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

# 最快+對照,平均+對照,對照-最快,對照-平均

# GA


def test():
    chinese_str = random_text()
    kb = Keyboard()
    kb.display_keyboard()
    print(f"Total distance: {check_total_distance(kb, chinese_str)}")
    kb = Keyboard()
    kb.swap('Q', 'J')
    kb.swap('A', 'K')
    kb.swap('R', 'B')
    kb.display_keyboard()
    print(f"Total distance: {check_total_distance(kb, chinese_str)}")


def main():
    global unicode2cangjie
    unicode2cangjie = read_json(r"dataset\cangjie\unicode2cangjie.json")
    test()



if __name__ == "__main__":
    main()
