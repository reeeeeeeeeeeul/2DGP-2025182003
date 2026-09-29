import math

from pico2d import *


open_canvas(800, 600)
character = load_image('character.png')


def draw_character(x, y):
	clear_canvas()
	character.draw(x, y)
	update_canvas()
	delay(0.01)


def move_circle():
	for degree in range(0, 360, 5):
		radians = math.radians(degree)
		x = 400 + 200 * math.cos(radians)
		y = 300 + 200 * math.sin(radians)
		draw_character(x, y)


def move_rectangle():
	for x in range(100, 701, 5):
		draw_character(x, 500)
	for y in range(500, 101, -5):
		draw_character(700, y)
	for x in range(700, 99, -5):
		draw_character(x, 100)
	for y in range(100, 501, 5):
		draw_character(100, y)


def move_triangle():
	for i in range(0, 401, 5):
		draw_character(400 - i * 0.5, 100 + i)
	for x in range(200, 601, 5):
		draw_character(x, 500)
	for i in range(0, 401, 5):
		draw_character(600 - i * 0.5, 500 - i)


while True:
	move_circle()
	move_rectangle()
	move_triangle()
