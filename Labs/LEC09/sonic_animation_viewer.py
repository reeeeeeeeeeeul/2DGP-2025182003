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


def make_row_frames(top, frame_height, x_ranges):
    source_y = SPRITE_SHEET_HEIGHT - top - frame_height
    return [
        (
            left,
            source_y,
            right - left + 1,
            frame_height,
        )
        for left, right in x_ranges
    ]


ANIMATIONS = [
    ('walk', make_row_frames(39, 39, [(0, 29), (30, 57), (58, 87), (88, 117), (118, 147), (148, 179), (180, 207), (208, 239), (240, 269), (270, 293), (294, 330)]), FRAME_DURATION),
    ('run', make_row_frames(79, 39, [(8, 33), (37, 63), (65, 95), (97, 133), (135, 166), (170, 201), (206, 231), (238, 261), (263, 292), (295, 330), (334, 365), (370, 398)]), FRAME_DURATION),
    ('jump', make_row_frames(121, 43, [(1, 33), (39, 73), (89, 123), (130, 163), (181, 214), (228, 260)]), FRAME_DURATION),
    ('roll', make_row_frames(167, 33, [(1, 29), (35, 63), (67, 96), (98, 128), (131, 159), (162, 190), (193, 222), (230, 260), (268, 297)]), FRAME_DURATION),
    ('spin', make_row_frames(206, 27, [(1, 30), (36, 64), (70, 98), (105, 133), (139, 167), (174, 202)]), FRAME_DURATION),
    ('crouch', make_row_frames(238, 36, [(1, 29), (36, 65), (74, 104), (111, 141), (149, 178), (186, 216)]), FRAME_DURATION),
    ('fall', make_row_frames(283, 35, [(1, 29), (36, 65), (72, 110), (123, 161), (172, 210), (218, 255)]), FRAME_DURATION),
    ('back', make_row_frames(326, 45, [(1, 24), (31, 59), (65, 84), (90, 114), (119, 143), (149, 168), (184, 223), (232, 270)]), FRAME_DURATION),
    ('idle', make_row_frames(377, 40, [(1, 27), (31, 61), (64, 94), (99, 131), (136, 167), (176, 208), (217, 249), (254, 286)]), FRAME_DURATION),
]


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
        source_width / source_height * FRAME_HEIGHT * DISPLAY_SCALE,
        FRAME_HEIGHT * DISPLAY_SCALE,
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


def advance_animation(
    delta_time,
    state,
    action_index,
    frame_index,
    repeat_count,
    frame_elapsed,
    wait_elapsed,
):
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

    return (
        state,
        action_index,
        frame_index,
        repeat_count,
        frame_elapsed,
        wait_elapsed,
    )


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
        (
            state,
            action_index,
            frame_index,
            repeat_count,
            frame_elapsed,
            wait_elapsed,
        ) = advance_animation(
            delta_time,
            state,
            action_index,
            frame_index,
            repeat_count,
            frame_elapsed,
            wait_elapsed,
        )
        clear_canvas()
        draw_frame(sprite_sheet, ANIMATIONS[action_index][1][frame_index])
        update_canvas()
        delay(0.01)

    del sprite_sheet
    close_canvas()


if __name__ == '__main__':
    main()
