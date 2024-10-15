# encoding: utf-8
from math import sqrt
import json

class Keyboard():
    @classmethod
    def set_new_keyboard(cls,DNA_key_list:list):
        new_keyboard = {}
        for DNA_key in DNA_key_list:
            for key,pos in DNA_key.items():
                if pos not in new_keyboard.values():
                    new_keyboard[key] = pos
        set_pos=set(new_keyboard.values())
        set_key=set(new_keyboard.keys())
        unset_key = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - set_key
        unset_value = set(range(26)) - set_pos
        for key in unset_key:
            new_keyboard[key] = unset_value.pop()
        return new_keyboard

    Total_Distance = 0

    def __init__(self, finger_group: list = None, finger_default_key=None, keyboard: dict = None):
        if finger_group:
            self.finger_group = finger_group
        else:
            self.finger_group = [
                0, 1, 2, 3, 3, 4, 4, 5, 6, 7,
                0, 1, 2, 3, 3, 4, 4, 5, 6,
                0, 1, 2, 3, 3, 4, 4
            ]
        if finger_default_key:
            self.finger_key = finger_default_key
        else:
            self.finger_key = [None]*8
        if keyboard:
            self.keyboard = keyboard
        else:
            self.keyboard = {
                'Q': 0, 'W': 1, 'E': 2, 'R': 3, 'T': 4, 'Y': 5, 'U': 6, 'I': 7, 'O': 8, 'P': 9,
                'A': 10, 'S': 11, 'D': 12, 'F': 13, 'G': 14, 'H': 15, 'J': 16, 'K': 17, 'L': 18,
                'Z': 19, 'X': 20, 'C': 21, 'V': 22, 'B': 23, 'N': 24, 'M': 25
            }

    rows_num_keys = [0, 10, 19, 26]
    row_start = [0, 1, 3]

    def __str__(self):
        s = ""
        key_list = list(self.keyboard.keys())
        pos_list = list(self.keyboard.values())
        row = 0
        for row_num in range(3):
            s += "\n"+" "*(row+row-1)
            for key_pos in range(self.rows_num_keys[row], self.rows_num_keys[row+1]):
                s+="   "+key_list[pos_list.index(key_pos)]
            row += 1
        return s

    def get_y(self, w_pos):
        return (w_pos > 18) + (w_pos > 9)

    def distance(self, key1, key2):
        key1_y = self.get_y(self.keyboard[key1])
        key2_y = self.get_y(self.keyboard[key2])
        key1_x = 4 * (self.keyboard[key1] -
                      self.rows_num_keys[key1_y]) + self.row_start[key1_y]
        key2_x = 4 * (self.keyboard[key2] -
                      self.rows_num_keys[key2_y]) + self.row_start[key2_y]
        return sqrt((key1_x - key2_x)**2 + (4*key1_y - 4*key2_y)**2)

    def finger_distance(self, key):
        try:
            key_pos = self.keyboard[key]
            finger = self.finger_group[key_pos]
        except KeyError:
            print(f"Key {key} not found in keyboard")
            return 0
        last_finger_key = self.finger_key[finger]
        self.finger_key[finger] = key
        if last_finger_key is None:
            return 0
        return self.distance(key, last_finger_key)

    def get_finger_key_group(self):
        key_gp_by_finger = [{}, {}, {}, {}, {}, {}, {}, {}]
        for key in self.keyboard.keys():
            pos = self.keyboard[key]
            key_gp_by_finger[self.finger_group[pos]][key] = pos
        return key_gp_by_finger

    def swap(self, w1, w2):
        self.keyboard[w1], self.keyboard[w2] = self.keyboard[w2], self.keyboard[w1]

    def save(self, filename,t):
        data = {'Keybard':self.keyboard, 'FingerGroup':self.finger_group, 'FingerKey':self.finger_key}
        with open(rf'result/{t}/{filename}_{t}.json', 'w') as file:
            file.write(json.dumps(data))
    
    def read(self, filename):
        with open(filename, 'r') as file:
            data = json.loads(file.read())
            self.keyboard = data['Keyboard']
            self.finger_group = data['FingerGroup']
            self.finger_key = data['FingerKey']


def main():
    kb = Keyboard()
    print(kb.get_finger_key_group())


if __name__ == "__main__":
    main()
