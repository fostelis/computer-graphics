import sys
import pygame

pygame.init()

window_width = 1000
window_height = 700
canvas_width = 700
panel_width = window_width - canvas_width

cell_size = 20
grid_width = canvas_width // cell_size
grid_height = window_height // cell_size

white = (255, 255, 255)
black = (0, 0, 0)
light_gray = (240, 240, 240)
gray = (200, 200, 200)
blue = (100, 180, 255)
red = (255, 89, 94)
green = (138, 201, 38)
yellow = (255, 202, 58)
purple = (187, 107, 217)
orange = (255, 158, 74)
cyan = (0, 188, 212)

colors = [
    black,
    red,
    green,
    blue,
    yellow,
    purple,
    orange,
    cyan,
    white,
]

color_names = [
    "Чёрный",
    "Красный",
    "Зелёный",
    "Синий",
    "Жёлтый",
    "Фиолетовый",
    "Оранжевый",
    "Бирюзовый",
    "Белый",
]

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Заливка")

title_font = pygame.font.SysFont("arial", 30)
header_font = pygame.font.SysFont("arial", 22)
text_font = pygame.font.SysFont("arial", 16)

draw_button = pygame.Rect(canvas_width + 30, 120, 200, 40)
fill_button = pygame.Rect(canvas_width + 30, 175, 200, 40)

grid = [
    [white for _ in range(grid_width)]
    for _ in range(grid_height)
]

current_color = black
current_mode = "draw"
mouse_pressed = False
last_drawn_cell = None


def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            cell_rect = pygame.Rect(
                x * cell_size,
                y * cell_size,
                cell_size,
                cell_size,
            )

            pygame.draw.rect(
                screen,
                grid[y][x],
                cell_rect,
            )
            pygame.draw.rect(
                screen,
                black,
                cell_rect,
                1,
            )


def get_color_rect(color_index):
    row = color_index // 2
    column = color_index % 2

    return pygame.Rect(
        canvas_width + 25 + column * 135,
        275 + row * 50,
        125,
        40,
    )


def draw_mode_buttons():
    draw_button_color = blue if current_mode == "draw" else gray
    fill_button_color = blue if current_mode == "fill" else gray

    pygame.draw.rect(
        screen,
        draw_button_color,
        draw_button,
        border_radius=6,
    )
    pygame.draw.rect(
        screen,
        black,
        draw_button,
        2,
        border_radius=6,
    )

    pygame.draw.rect(
        screen,
        fill_button_color,
        fill_button,
        border_radius=6,
    )
    pygame.draw.rect(
        screen,
        black,
        fill_button,
        2,
        border_radius=6,
    )

    draw_text = text_font.render(
        "Рисование",
        True,
        black,
    )
    fill_text = text_font.render(
        "Заливка",
        True,
        black,
    )

    screen.blit(
        draw_text,
        (
            draw_button.centerx - draw_text.get_width() // 2,
            draw_button.centery - draw_text.get_height() // 2,
        ),
    )
    screen.blit(
        fill_text,
        (
            fill_button.centerx - fill_text.get_width() // 2,
            fill_button.centery - fill_text.get_height() // 2,
        ),
    )


def draw_color_palette():
    for color_index, color in enumerate(colors):
        color_rect = get_color_rect(color_index)

        if color == current_color:
            pygame.draw.rect(
                screen,
                blue,
                color_rect,
                3,
                border_radius=6,
            )
        else:
            pygame.draw.rect(
                screen,
                gray,
                color_rect,
                1,
                border_radius=6,
            )

        preview_rect = pygame.Rect(
            color_rect.x + 5,
            color_rect.y + 5,
            30,
            30,
        )

        pygame.draw.rect(
            screen,
            color,
            preview_rect,
        )
        pygame.draw.rect(
            screen,
            black,
            preview_rect,
            1,
        )

        name_text = text_font.render(
            color_names[color_index],
            True,
            black,
        )

        screen.blit(
            name_text,
            (color_rect.x + 42, color_rect.y + 11),
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
        blue,
        (canvas_width, 0),
        (canvas_width, window_height),
        2,
    )

    title_text = title_font.render(
        "Заливка",
        True,
        black,
    )
    screen.blit(
        title_text,
        (canvas_width + 20, 20),
    )

    pygame.draw.line(
        screen,
        gray,
        (canvas_width + 20, 65),
        (window_width - 20, 65),
    )

    mode_header = header_font.render(
        "Режим",
        True,
        black,
    )
    screen.blit(
        mode_header,
        (canvas_width + 20, 80),
    )

    draw_mode_buttons()

    colors_header = header_font.render(
        "Цвет",
        True,
        black,
    )
    screen.blit(
        colors_header,
        (canvas_width + 20, 235),
    )

    draw_color_palette()

    instruction_header = header_font.render(
        "Управление",
        True,
        black,
    )
    screen.blit(
        instruction_header,
        (canvas_width + 20, 535),
    )

    instructions = [
        "Выберите цвет и нарисуйте контур",
        "Переключитесь в режим заливки",
        "Нажмите внутри замкнутой области",
    ]

    y_offset = 570

    for instruction in instructions:
        instruction_text = text_font.render(
            instruction,
            True,
            black,
        )
        screen.blit(
            instruction_text,
            (canvas_width + 25, y_offset),
        )
        y_offset += 25


def flood_fill(start_x, start_y, replacement_color):
    target_color = grid[start_y][start_x]

    if target_color == replacement_color:
        return

    cells_to_fill = [(start_x, start_y)]

    while cells_to_fill:
        x, y = cells_to_fill.pop()

        if x < 0 or x >= grid_width:
            continue

        if y < 0 or y >= grid_height:
            continue

        if grid[y][x] != target_color:
            continue

        grid[y][x] = replacement_color

        cells_to_fill.append((x + 1, y))
        cells_to_fill.append((x - 1, y))
        cells_to_fill.append((x, y + 1))
        cells_to_fill.append((x, y - 1))


def get_clicked_color(mouse_position):
    for color_index, color in enumerate(colors):
        color_rect = get_color_rect(color_index)

        if color_rect.collidepoint(mouse_position):
            return color

    return None


def get_grid_cell(mouse_position):
    mouse_x, mouse_y = mouse_position

    if mouse_x < 0 or mouse_x >= canvas_width:
        return None

    if mouse_y < 0 or mouse_y >= window_height:
        return None

    grid_x = mouse_x // cell_size
    grid_y = mouse_y // cell_size

    return grid_x, grid_y


def draw_in_cell(mouse_position):
    global last_drawn_cell

    clicked_cell = get_grid_cell(mouse_position)

    if clicked_cell is None:
        return

    if clicked_cell == last_drawn_cell:
        return

    grid_x, grid_y = clicked_cell
    grid[grid_y][grid_x] = current_color
    last_drawn_cell = clicked_cell


def handle_panel_click(mouse_position):
    global current_mode
    global current_color

    if draw_button.collidepoint(mouse_position):
        current_mode = "draw"
        return

    if fill_button.collidepoint(mouse_position):
        current_mode = "fill"
        return

    clicked_color = get_clicked_color(mouse_position)

    if clicked_color is not None:
        current_color = clicked_color


def handle_canvas_click(mouse_position):
    clicked_cell = get_grid_cell(mouse_position)

    if clicked_cell is None:
        return

    grid_x, grid_y = clicked_cell

    if current_mode == "draw":
        draw_in_cell(mouse_position)
    else:
        flood_fill(
            grid_x,
            grid_y,
            current_color,
        )


def main():
    global mouse_pressed
    global last_drawn_cell

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
                    continue

                mouse_pressed = True

                if event.pos[0] < canvas_width:
                    handle_canvas_click(event.pos)
                else:
                    handle_panel_click(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed = False
                    last_drawn_cell = None

            elif event.type == pygame.MOUSEMOTION:
                if mouse_pressed and current_mode == "draw":
                    draw_in_cell(event.pos)

        screen.fill(white)
        draw_grid()
        draw_tool_panel()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
