# encoding: utf-8
import json
from random import choice
import displaykeyboard

last_changjie = ""
pattern = r'[\t ，。,.:：;；!！?？—\-「」『』【】《》〈〉〔〕〖〗〘〙〚〛〝〞〟〰‥…‧﹏﹑﹔﹖﹪﹫？｡。\\/:*?"<>|\(\)─（）／＊、]'
def chinese_to_unicode(char):
    return f'{ord(char):04x}'

def read_json(fileName):
    with open(rf"{fileName}", 'r', encoding='utf-8-sig') as file:
        return json.load(file)


def check_total_distance(chinese_str):
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
                displaykeyboard.init_keyboard, current_key_chanjie[key - 1],
                current_key_chanjie[key])
        last_changjie = current_key_chanjie[-1]
    return total_distance

def test():
    chinese_str = "[(灶，。,.:：)]好"

    print(f"Total distance: {check_total_distance(chinese_str)}")


def main():
    global unicode2cangjie
    unicode2cangjie = read_json(r"dataset\cangjie\unicode2cangjie.json")
    test()

if __name__ == "__main__":
    main()
