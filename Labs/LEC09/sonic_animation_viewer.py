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
REPEAT_LIMIT = 5
WAIT_DURATION = 1.0
PLAYING = 'playing'
WAITING = 'waiting'


def resource_path(file_name):
    return Path(__file__).resolve().parent / file_name


def make_row_frames(top, frame_count):
    source_y = SPRITE_SHEET_HEIGHT - top - FRAME_HEIGHT
    return [
        (
            index * FRAME_WIDTH,
            source_y,
            min(FRAME_WIDTH, SPRITE_SHEET_WIDTH - index * FRAME_WIDTH),
            FRAME_HEIGHT,
        )
        for index in range(frame_count)
    ]


ANIMATIONS = [
    ('run', make_row_frames(35, 10), FRAME_DURATION),
    ('run_fast', make_row_frames(83, 10), FRAME_DURATION),
    ('jump', make_row_frames(126, 7), FRAME_DURATION),
    ('roll', make_row_frames(174, 8), FRAME_DURATION),
    ('spin', make_row_frames(222, 6), FRAME_DURATION),
    ('crouch', make_row_frames(271, 7), FRAME_DURATION),
    ('fall', make_row_frames(319, 7), FRAME_DURATION),
    ('back', make_row_frames(367, 7), FRAME_DURATION),
    ('idle', make_row_frames(414, 8), FRAME_DURATION),
]


def handle_events():
def validate_animations(sheet_width, sheet_height):
    if not ANIMATIONS:
        raise ValueError('애니메이션 동작이 정의되지 않았습니다.')

    for action_name, frames, frame_duration in ANIMATIONS:
        if not action_name or not frames:
            raise ValueError('이름 또는 프레임이 없는 동작이 있습니다.')
        if frame_duration <= 0:
            raise ValueError(f'{action_name} 동작의 프레임 시간이 올바르지 않습니다.')

        for source_x, source_y, source_width, source_height in frames:
            if source_x < 0 or source_y < 0:
                raise ValueError(f'{action_name} 동작에 음수 좌표가 있습니다.')
            if source_x + source_width > sheet_width:
                raise ValueError(f'{action_name} 동작이 이미지 오른쪽을 벗어납니다.')
            if source_y + source_height > sheet_height:
                raise ValueError(f'{action_name} 동작이 이미지 위쪽을 벗어납니다.')


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


def advance_frame(
    frame_index,
    frame_elapsed,
    delta_time,
    frames,
    frame_duration,
    repeat_count,
):
    completed = False
    frame_elapsed += delta_time
    while frame_elapsed >= frame_duration:
        frame_elapsed -= frame_duration
        if frame_index < len(frames) - 1:
            frame_index += 1
            continue

        repeat_count += 1
        if repeat_count < REPEAT_LIMIT:
            frame_index = 0
        else:
            completed = True
            break
    return frame_index, frame_elapsed, repeat_count, completed


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sprite_path = resource_path('sonic-sprite.png')
    if not sprite_path.exists():
        close_canvas()
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {sprite_path}')

    sprite_sheet = load_image(str(sprite_path))
    validate_animations(sprite_sheet.w, sprite_sheet.h)
    frame_index = 0
    frame_elapsed = 0.0
    repeat_count = 0
    action_index = 0
    state = PLAYING
    wait_elapsed = 0.0
    previous_time = get_time()
    running = True
    while running:
        current_time = get_time()
        delta_time = current_time - previous_time
        previous_time = current_time
        running = handle_events()
        if state == PLAYING:
            frames = ANIMATIONS[action_index][1]
            frame_index, frame_elapsed, repeat_count, completed = advance_frame(
                frame_index,
                frame_elapsed,
                delta_time,
                frames,
                ANIMATIONS[action_index][2],
                repeat_count,
            )
            if completed:
                state = WAITING
                wait_elapsed = 0.0
        elif state == WAITING:
            wait_elapsed += delta_time
            if wait_elapsed >= WAIT_DURATION:
                action_index = (action_index + 1) % len(ANIMATIONS)
                frame_index = 0
                frame_elapsed = 0.0
                repeat_count = 0
                wait_elapsed = 0.0
                state = PLAYING
        clear_canvas()
        draw_frame(sprite_sheet, ANIMATIONS[action_index][1][frame_index])
        update_canvas()
        delay(0.01)

    del sprite_sheet
    close_canvas()


if __name__ == '__main__':
    main()
