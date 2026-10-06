from pathlib import Path

from pico2d import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
DISPLAY_SCALE = 3
FRAME_WIDTH = 40
FRAME_HEIGHT = 50
SPRITE_SHEET_WIDTH = 399
SPRITE_SHEET_HEIGHT = 525
FRAME_DURATION = 0.12


def resource_path(file_name):
    return Path(__file__).resolve().parent / file_name


def make_row_frames(top, frame_count):
    source_y = SPRITE_SHEET_HEIGHT - top - FRAME_HEIGHT
    return [
        (index * FRAME_WIDTH, source_y, FRAME_WIDTH, FRAME_HEIGHT)
        for index in range(frame_count)
    ]


ANIMATIONS = [
    ('run', make_row_frames(35, 10), FRAME_DURATION),
]


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
    return True


def draw_frame(sprite_sheet, frame):
    source_x, source_y, source_width, source_height = frame
    sprite_sheet.clip_draw(
        source_x,
        source_y,
        source_width,
        source_height,
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT // 2,
        source_width * DISPLAY_SCALE,
        source_height * DISPLAY_SCALE,
    )


def advance_frame(frame_index, frame_elapsed, delta_time, frames, frame_duration):
    frame_elapsed += delta_time
    while frame_elapsed >= frame_duration:
        frame_elapsed -= frame_duration
        frame_index = (frame_index + 1) % len(frames)
    return frame_index, frame_elapsed


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sprite_path = resource_path('sonic-sprite.png')
    if not sprite_path.exists():
        close_canvas()
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {sprite_path}')

    sprite_sheet = load_image(str(sprite_path))
    frame_index = 0
    frame_elapsed = 0.0
    previous_time = get_time()
    running = True
    while running:
        current_time = get_time()
        delta_time = current_time - previous_time
        previous_time = current_time
        running = handle_events()
        frames = ANIMATIONS[0][1]
        frame_index, frame_elapsed = advance_frame(
            frame_index,
            frame_elapsed,
            delta_time,
            frames,
            ANIMATIONS[0][2],
        )
        clear_canvas()
        draw_frame(sprite_sheet, ANIMATIONS[0][1][frame_index])
        update_canvas()
        delay(0.01)

    del sprite_sheet
    close_canvas()


if __name__ == '__main__':
    main()
