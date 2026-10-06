from pathlib import Path

from pico2d import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700


def resource_path(file_name):
    return Path(__file__).resolve().parent / file_name


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
    return True


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    running = True
    while running:
        running = handle_events()
        clear_canvas()
        update_canvas()
        delay(0.01)

    close_canvas()


if __name__ == '__main__':
    main()
