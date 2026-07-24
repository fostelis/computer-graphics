import sys
import pygame

pygame.init()

window_width = 1000
window_height = 700
canvas_width = 700
panel_width = window_width - canvas_width

min_grid_size = 5
max_grid_size = 50
grid_size = 10

center_x = canvas_width // 2
center_y = window_height // 2

white = (255, 255, 255)
light_gray = (240, 240, 240)
grid_color = (220, 220, 220)
border_color = (180, 180, 180)
black = (0, 0, 0)
red = (255, 80, 80)
blue = (100, 180, 255)
input_color = (225, 225, 225)

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Алгоритм Брезенхема")

title_font = pygame.font.SysFont("arial", 28)
header_font = pygame.font.SysFont("arial", 22)
text_font = pygame.font.SysFont("arial", 16)
small_font = pygame.font.SysFont("arial", 12)
input_font = pygame.font.SysFont("arial", 18)

input_boxes = {
    "x_0": pygame.Rect(canvas_width + 50, 150, 80, 35),
    "y_0": pygame.Rect(canvas_width + 50, 200, 80, 35),
    "x_1": pygame.Rect(canvas_width + 50, 250, 80, 35),
    "y_1": pygame.Rect(canvas_width + 50, 300, 80, 35),
}

input_values = {
    "x_0": "",
    "y_0": "",
    "x_1": "",
    "y_1": "",
}

draw_button = pygame.Rect(canvas_width + 50, 350, 180, 40)

active_input = None
line_points = []
error_message = ""


def bresenham_line(x_0, y_0, x_1, y_1):
    points = []

    delta_x = abs(x_1 - x_0)
    delta_y = abs(y_1 - y_0)

    step_x = 1 if x_0 < x_1 else -1
    step_y = 1 if y_0 < y_1 else -1

    error = delta_x - delta_y

    while True:
        points.append((x_0, y_0))

        if x_0 == x_1 and y_0 == y_1:
            break

        doubled_error = 2 * error

        if doubled_error > -delta_y:
            error -= delta_y
            x_0 += step_x

        if doubled_error < delta_x:
            error += delta_x
            y_0 += step_y

    return points


def logical_to_screen(x, y):
    screen_x = center_x + x * grid_size
    screen_y = center_y - y * grid_size

    return screen_x, screen_y


def get_visible_range():
    horizontal_range = canvas_width // (2 * grid_size)
    vertical_range = window_height // (2 * grid_size)

    return horizontal_range, vertical_range


def get_label_step():
    target_distance = 60
    step = max(1, round(target_distance / grid_size))

    if step <= 1:
        return 1

    if step <= 2:
        return 2

    if step <= 5:
        return 5

    return ((step + 9) // 10) * 10


def draw_grid():
    pygame.draw.rect(
        screen,
        white,
        pygame.Rect(0, 0, canvas_width, window_height),
    )

    first_vertical_line = center_x % grid_size
    first_horizontal_line = center_y % grid_size

    for x in range(first_vertical_line, canvas_width, grid_size):
        pygame.draw.line(
            screen,
            grid_color,
            (x, 0),
            (x, window_height),
        )

    for y in range(first_horizontal_line, window_height, grid_size):
        pygame.draw.line(
            screen,
            grid_color,
            (0, y),
            (canvas_width, y),
        )

    pygame.draw.line(
        screen,
        black,
        (0, center_y),
        (canvas_width, center_y),
        2,
    )
    pygame.draw.line(
        screen,
        black,
        (center_x, 0),
        (center_x, window_height),
        2,
    )

    draw_axis_labels()


def draw_axis_labels():
    horizontal_range, vertical_range = get_visible_range()
    label_step = get_label_step()

    x_axis_text = small_font.render("x", True, black)
    y_axis_text = small_font.render("y", True, black)

    screen.blit(
        x_axis_text,
        (canvas_width - 20, center_y + 8),
    )
    screen.blit(
        y_axis_text,
        (center_x + 8, 10),
    )

    for x in range(-horizontal_range, horizontal_range + 1, label_step):
        if x == 0:
            continue

        screen_x, _ = logical_to_screen(x, 0)

        pygame.draw.line(
            screen,
            black,
            (screen_x, center_y - 4),
            (screen_x, center_y + 4),
        )

        number_text = small_font.render(str(x), True, black)
        screen.blit(
            number_text,
            (screen_x - number_text.get_width() // 2, center_y + 8),
        )

    for y in range(-vertical_range, vertical_range + 1, label_step):
        if y == 0:
            continue

        _, screen_y = logical_to_screen(0, y)

        pygame.draw.line(
            screen,
            black,
            (center_x - 4, screen_y),
            (center_x + 4, screen_y),
        )

        number_text = small_font.render(str(y), True, black)
        screen.blit(
            number_text,
            (center_x + 8, screen_y - number_text.get_height() // 2),
        )

    zero_text = small_font.render("0", True, black)
    screen.blit(
        zero_text,
        (center_x + 6, center_y + 6),
    )


def draw_line():
    for x, y in line_points:
        screen_x, screen_y = logical_to_screen(x, y)

        pixel_rect = pygame.Rect(
            screen_x - grid_size // 2,
            screen_y - grid_size // 2,
            grid_size,
            grid_size,
        )

        pygame.draw.rect(
            screen,
            red,
            pixel_rect,
        )
        pygame.draw.rect(
            screen,
            black,
            pixel_rect,
            1,
        )


def draw_input_boxes():
    labels = {
        "x_0": "x0",
        "y_0": "y0",
        "x_1": "x1",
        "y_1": "y1",
    }

    for key, rect in input_boxes.items():
        label_text = text_font.render(labels[key], True, black)

        screen.blit(
            label_text,
            (canvas_width + 20, rect.y + 8),
        )

        border = blue if active_input == key else border_color

        pygame.draw.rect(
            screen,
            input_color,
            rect,
            border_radius=3,
        )
        pygame.draw.rect(
            screen,
            border,
            rect,
            2,
            border_radius=3,
        )

        value_text = input_font.render(
            input_values[key],
            True,
            black,
        )

        screen.blit(
            value_text,
            (rect.x + 6, rect.y + 7),
        )


def draw_tool_panel():
    panel_rect = pygame.Rect(
        canvas_width,
        0,
        panel_width,
        window_height,
    )

    pygame.draw.rect(
        screen,
        light_gray,
        panel_rect,
    )
    pygame.draw.line(
        screen,
        border_color,
        (canvas_width, 0),
        (canvas_width, window_height),
        2,
    )

    title_text = title_font.render(
        "Алгоритм Брезенхема",
        True,
        black,
    )
    screen.blit(
        title_text,
        (canvas_width + 20, 20),
    )

    pygame.draw.line(
        screen,
        border_color,
        (canvas_width + 20, 70),
        (window_width - 20, 70),
    )

    coordinates_text = header_font.render(
        "Координаты",
        True,
        black,
    )
    screen.blit(
        coordinates_text,
        (canvas_width + 20, 100),
    )

    draw_input_boxes()

    pygame.draw.rect(
        screen,
        blue,
        draw_button,
        border_radius=5,
    )
    pygame.draw.rect(
        screen,
        black,
        draw_button,
        2,
        border_radius=5,
    )

    button_text = text_font.render(
        "Построить линию",
        True,
        black,
    )
    button_x = draw_button.centerx - button_text.get_width() // 2
    button_y = draw_button.centery - button_text.get_height() // 2

    screen.blit(
        button_text,
        (button_x, button_y),
    )

    instruction_header = header_font.render(
        "Управление",
        True,
        black,
    )
    screen.blit(
        instruction_header,
        (canvas_width + 20, 420),
    )

    instructions = [
        "Введите координаты точек",
        "Нажмите «Построить линию»",
        "Колёсико меняет масштаб",
    ]

    y_offset = 455

    for instruction in instructions:
        instruction_text = text_font.render(
            instruction,
            True,
            black,
        )
        screen.blit(
            instruction_text,
            (canvas_width + 30, y_offset),
        )
        y_offset += 24

    scale_text = text_font.render(
        f"Масштаб, {grid_size} px",
        True,
        black,
    )
    screen.blit(
        scale_text,
        (canvas_width + 30, 545),
    )

    if line_points:
        points_text = text_font.render(
            f"Точек, {len(line_points)}",
            True,
            black,
        )
        screen.blit(
            points_text,
            (canvas_width + 30, 575),
        )

    if error_message:
        message_text = small_font.render(
            error_message,
            True,
            red,
        )
        screen.blit(
            message_text,
            (canvas_width + 20, 620),
        )


def build_line():
    global line_points
    global error_message

    try:
        x_0 = int(input_values["x_0"])
        y_0 = int(input_values["y_0"])
        x_1 = int(input_values["x_1"])
        y_1 = int(input_values["y_1"])
    except ValueError:
        error_message = "Введите целые числа"
        return

    line_points = bresenham_line(
        x_0,
        y_0,
        x_1,
        y_1,
    )
    error_message = ""

    print(f"линия от ({x_0}, {y_0}) до ({x_1}, {y_1})")

    for point in line_points:
        print(point)

    print(f"всего точек, {len(line_points)}")


def handle_mouse_click(mouse_position):
    global active_input

    if draw_button.collidepoint(mouse_position):
        build_line()
        active_input = None
        return

    for key, rect in input_boxes.items():
        if rect.collidepoint(mouse_position):
            active_input = key
            return

    active_input = None


def handle_keyboard_input(event):
    global active_input

    if active_input is None:
        return

    if event.key == pygame.K_RETURN:
        build_line()
        active_input = None
        return

    if event.key == pygame.K_BACKSPACE:
        input_values[active_input] = input_values[active_input][:-1]
        return

    if event.unicode.isdigit():
        input_values[active_input] += event.unicode
        return

    if event.unicode == "-" and not input_values[active_input]:
        input_values[active_input] = "-"


def change_scale(scroll_direction):
    global grid_size

    previous_grid_size = grid_size
    grid_size += scroll_direction * 5
    grid_size = max(min_grid_size, min(grid_size, max_grid_size))

    if grid_size != previous_grid_size:
        print(f"масштаб, {grid_size} px")


def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    handle_mouse_click(event.pos)

            elif event.type == pygame.MOUSEWHEEL:
                change_scale(event.y)

            elif event.type == pygame.KEYDOWN:
                handle_keyboard_input(event)

        screen.fill(light_gray)
        draw_grid()
        draw_line()
        draw_tool_panel()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
