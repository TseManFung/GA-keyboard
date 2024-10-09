# encoding: utf-8
from math import sqrt

rows_num_keys = [0, 10, 19, 26]

init_keyboard = {
    'Q': 0, 'W': 1, 'E': 2, 'R': 3, 'T': 4, 'Y': 5, 'U': 6, 'I': 7, 'O': 8, 'P': 9,
    'A': 10, 'S': 11, 'D': 12, 'F': 13, 'G': 14, 'H': 15, 'J': 16, 'K': 17, 'L': 18,
    'Z': 19, 'X': 20, 'C': 21, 'V': 22, 'B': 23, 'N': 24, 'M': 25
}


def display_keyboard(keyboard):
    key_list = list(keyboard.keys())
    pos_list = list(keyboard.values())
    row = 0
    for row_num in range(3):
        print(" "*(row+row-1), end="")
        for key_pos in range(rows_num_keys[row], rows_num_keys[row+1]):
            print("   "+key_list[pos_list.index(key_pos)], end="")
        print("")
        row += 1


def get_y(w_pos):
    return (w_pos > 18) + (w_pos > 9)


def distance(keyboard, w1, w2):
    row_start = [0, 1, 3]
    w1_y = get_y(keyboard[w1])
    w2_y = get_y(keyboard[w2])
    w1_x = 4*(keyboard[w1] - rows_num_keys[w1_y]) + row_start[w1_y]
    w2_x = 4*(keyboard[w2] - rows_num_keys[w2_y]) + row_start[w2_y]
    return sqrt((w1_x - w2_x)**2 + (4*w1_y - 4*w2_y)**2)


def swap(keyboard, w1, w2):
    keyboard[w1], keyboard[w2] = keyboard[w2], keyboard[w1]


def main():
    display_keyboard(init_keyboard)
    print(distance(init_keyboard, 'Q', 'Z'))
    swap(init_keyboard, 'Q', 'Z')
    display_keyboard(init_keyboard)
    print(distance(init_keyboard, 'Q', 'Z'))


if __name__ == "__main__":
    main()
