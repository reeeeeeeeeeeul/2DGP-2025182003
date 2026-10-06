from pathlib import Path

from pico2d import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
DISPLAY_SCALE = 3
FRAME_WIDTH = 40
FRAME_HEIGHT = 50
SPRITE_SHEET_WIDTH = 399
SPRITE_SHEET_HEIGHT = 525


def resource_path(file_name):
    return Path(__file__).resolve().parent / file_name


def make_row_frames(top, frame_count):
    source_y = SPRITE_SHEET_HEIGHT - top - FRAME_HEIGHT
    return [
        (index * FRAME_WIDTH, source_y, FRAME_WIDTH, FRAME_HEIGHT)
        for index in range(frame_count)
    ]


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
    return True


def draw_sprite_sheet(sprite_sheet):
    sprite_sheet.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sprite_path = resource_path('sonic-sprite.png')
    if not sprite_path.exists():
        close_canvas()
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {sprite_path}')

    sprite_sheet = load_image(str(sprite_path))
    running = True
    while running:
        running = handle_events()
        clear_canvas()
        draw_sprite_sheet(sprite_sheet)
        update_canvas()
        delay(0.01)

    del sprite_sheet
    close_canvas()


if __name__ == '__main__':
    main()
