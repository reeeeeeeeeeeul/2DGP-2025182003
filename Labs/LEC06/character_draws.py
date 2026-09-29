# 실습 과제 진행
import math
from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')


def move_circle():
    print("circle")
    for deg in range(0, 360, 5):
        rad = math.radians(deg)
        x=400+200*math.cos(rad)
        y=400+200*math.sin(rad)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.1)
    pass


def draw_top():
    print("top")
    pass

def draw_right():
    print("right")
    pass

def draw_bottom():
    print("bottom")
    pass

def draw_left():
    print("left")
    pass


def move_rectangle():
    print("rectangle")
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()
    pass

def move_triangle():
    print("triangle")
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    pass