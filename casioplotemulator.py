import os
from characters import _get_char
WIDTH = 127
HEIGHT = 63

contents = [[0 for j in range(WIDTH)] for i in range(HEIGHT)]

def set_pixel(x, y):
    try:
        contents[y][x] = 1
    except:
        pass

def draw_string(x, y, text):
    def _draw_char(char_map) -> None:
        for y2, row in enumerate(char_map):
            for x2, pixel in enumerate(row):
                if pixel is True:
                    set_pixel(x + x2, y + y2)
    for char in text:
        char_map = _get_char(char)
        _draw_char(char_map)
        x += len(char_map[0])

def clear_screen():
    global contents
    contents = [[0 for j in range(WIDTH)] for i in range(HEIGHT)]

def show_screen():
    os.system("clear")
    for row in contents:
        for pixel in row:
            if pixel == 1: print("██", end="")
            else: print("  ", end="")
        print("hi")