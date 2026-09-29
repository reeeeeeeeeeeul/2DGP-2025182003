import math

from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')


def move_circle():
    print("circle")

    for deg in range(0, 360, 5):
        rad = math.radians(deg)

        x = 400 + 200 * math.cos(rad)
        y = 400 + 200 * math.sin(rad)

        draw_character(x, y)


def draw_top():
    for x in range(50, 750, 5):
        draw_character(x, 550)


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)


def draw_right():
    for y in range(550, 50, -5):
        draw_character(750, y)


def draw_bottom():
    for x in range(750, 50, -5):
        draw_character(x, 50)


def draw_left():
    for y in range(50, 550, 5):
        draw_character(50, y)


def move_rectangle():
    print("rectangle")
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()


def draw_a():
    print("a")

    for i in range(0, 401, 5):
        x = 400 - i * 0.5
        y = 100 + i

        draw_character(x, y)


def draw_b():
    print("b")

    for x in range(200, 601, 5):
        y = 500

        draw_character(x, y)


def draw_c():
    print("c")

    for i in range(0, 401, 5):
        x = 600 - i * 0.5
        y = 500 - i


def move_triangle():
    print("triangle")
    draw_a()
    draw_b()
    draw_c()


while True:
    move_circle()
    move_rectangle()
    move_triangle()