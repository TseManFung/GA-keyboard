# encoding: utf-8
from math import sqrt


class Keyboard():
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

    def display_keyboard(self):
        key_list = list(self.keyboard.keys())
        pos_list = list(self.keyboard.values())
        row = 0
        for row_num in range(3):
            print(" "*(row+row-1), end="")
            for key_pos in range(self.rows_num_keys[row], self.rows_num_keys[row+1]):
                print("   "+key_list[pos_list.index(key_pos)], end="")
            print("")
            row += 1

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
        key_pos = self.keyboard[key]
        finger = self.finger_group[key_pos]
        last_finger_key = self.finger_key[finger]
        self.finger_key[finger] = key
        if last_finger_key is None:
            return 0
        return self.distance(key, last_finger_key)

    def swap(self, w1, w2):
        self.keyboard[w1], self.keyboard[w2] = self.keyboard[w2], self.keyboard[w1]


def main():
    keyboard1 = Keyboard()
    keyboard1.display_keyboard()


if __name__ == "__main__":
    main()
