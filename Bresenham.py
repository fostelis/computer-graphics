import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 1000, 700
CANVAS_WIDTH = 700
GRID_SIZE = 5
GRID_OFFSET = 60
DARK_TEXT = (0, 0, 0)
LIGHT_BG = (240, 240, 240)
ACCENT = (100, 180, 255)
INPUT_BG = (220, 220, 220)
CENTER_X = CANVAS_WIDTH // 2
CENTER_Y = HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Алгоритм Брезенхема - Построение линии")
title_font = pygame.font.SysFont("arial", 28)
header_font = pygame.font.SysFont("arial", 22)
text_font = pygame.font.SysFont("arial", 16)
small_font = pygame.font.SysFont("arial", 12)
input_font = pygame.font.SysFont("arial", 18)
input_boxes = {
    'x0': pygame.Rect(CANVAS_WIDTH + 50, 150, 80, 35),
    'y0': pygame.Rect(CANVAS_WIDTH + 50, 200, 80, 35),
    'x1': pygame.Rect(CANVAS_WIDTH + 50, 250, 80, 35),
    'y1': pygame.Rect(CANVAS_WIDTH + 50, 300, 80, 35)
}
input_values = {'x0': '', 'y0': '', 'x1': '', 'y1': ''}
active_input = None
line_points = []
calculated_points = []

def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        points.append((x0, y0))
        print(f"({x0}, {y0})")
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points


def draw_grid():
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, CANVAS_WIDTH, HEIGHT))
    for x in range(0, CANVAS_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (220, 220, 220), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (220, 220, 220), (0, y), (CANVAS_WIDTH, y), 1)
    pygame.draw.line(screen, DARK_TEXT, (0, CENTER_Y), (CANVAS_WIDTH, CENTER_Y), 2)
    pygame.draw.line(screen, DARK_TEXT, (CENTER_X, 0), (CENTER_X, HEIGHT), 2)
    x_text = small_font.render("X", True, DARK_TEXT)
    y_text = small_font.render("Y", True, DARK_TEXT)
    screen.blit(x_text, (CANVAS_WIDTH - 20, CENTER_Y + 10))
    screen.blit(y_text, (CENTER_X + 10, 10))
    for i in range(-GRID_OFFSET, GRID_OFFSET + 1, 10):
        if i != 0:
            x_pos = CENTER_X + i * GRID_SIZE
            if 0 <= x_pos <= CANVAS_WIDTH:
                pygame.draw.line(screen, DARK_TEXT, (x_pos, CENTER_Y - 5), (x_pos, CENTER_Y + 5), 1)
                num_text = small_font.render(str(i), True, DARK_TEXT)
                screen.blit(num_text, (x_pos - 10, CENTER_Y + 10))
            y_pos = CENTER_Y - i * GRID_SIZE
            if 0 <= y_pos <= HEIGHT:
                pygame.draw.line(screen, DARK_TEXT, (CENTER_X - 5, y_pos), (CENTER_X + 5, y_pos), 1)
                num_text = small_font.render(str(i), True, DARK_TEXT)
                screen.blit(num_text, (CENTER_X + 10, y_pos - 10))
    zero_text = small_font.render("0", True, DARK_TEXT)
    screen.blit(zero_text, (CENTER_X + 5, CENTER_Y + 5))

def draw_line():
    if line_points:
        for i in range(len(line_points) - 1):
            x1, y1 = line_points[i]
            x2, y2 = line_points[i + 1]
            screen_x1 = CENTER_X + x1 * GRID_SIZE
            screen_y1 = CENTER_Y - y1 * GRID_SIZE
            screen_x2 = CENTER_X + x2 * GRID_SIZE
            screen_y2 = CENTER_Y - y2 * GRID_SIZE
            pygame.draw.line(screen, (255, 0, 0), (screen_x1, screen_y1), (screen_x2, screen_y2), 2)

def draw_tool_panel():
    pygame.draw.rect(screen, LIGHT_BG, (CANVAS_WIDTH, 0, WIDTH - CANVAS_WIDTH, HEIGHT))
    pygame.draw.line(screen, (200, 200, 200), (CANVAS_WIDTH, 0), (CANVAS_WIDTH, HEIGHT), 2)
    title = title_font.render("Алгоритм Брезенхема", True, DARK_TEXT)
    screen.blit(title, (CANVAS_WIDTH + 20, 20))
    pygame.draw.line(screen, (200, 200, 200), (CANVAS_WIDTH + 20, 70), (WIDTH - 20, 70), 1)
    header = header_font.render("Введите координаты:", True, DARK_TEXT)
    screen.blit(header, (CANVAS_WIDTH + 20, 100))
    labels = ["X0:", "Y0:", "X1:", "Y1:"]
    y_positions = [155, 205, 255, 305]
    for label, y_pos in zip(labels, y_positions):
        label_text = text_font.render(label, True, DARK_TEXT)
        screen.blit(label_text, (CANVAS_WIDTH + 20, y_pos))
    for key, rect in input_boxes.items():
        color = ACCENT if active_input == key else (180, 180, 180)
        pygame.draw.rect(screen, INPUT_BG, rect, border_radius=3)
        pygame.draw.rect(screen, color, rect, 2, border_radius=3)
        text_surface = input_font.render(input_values[key], True, DARK_TEXT)
        screen.blit(text_surface, (rect.x + 5, rect.y + 8))
    draw_button = pygame.Rect(CANVAS_WIDTH + 50, 350, 180, 40)
    pygame.draw.rect(screen, ACCENT, draw_button, border_radius=5)
    pygame.draw.rect(screen, DARK_TEXT, draw_button, 2, border_radius=5)
    button_text = text_font.render("Построить линию", True, DARK_TEXT)
    screen.blit(button_text, (CANVAS_WIDTH + 70, 360))
    header = header_font.render("Инструкция:", True, DARK_TEXT)
    screen.blit(header, (CANVAS_WIDTH + 20, 410))
    info_text = [
        f"- Введите координаты двух точек",
        f"- Нажмите на голубую кнопку",
        f"- Наблюдайте, как строится линия",
        f"- Вы молодец! =)",
        "",
    ]
    y_offset = 440
    for text in info_text:
        inst_text = text_font.render(text, True, DARK_TEXT)
        screen.blit(inst_text, (CANVAS_WIDTH + 30, y_offset))
        y_offset += 22

running = True
clock = pygame.time.Clock()
print("=" * 50)
print("АЛГОРИТМ БРЕЗЕНХЕМА")
print("Координаты точек линии будут выводиться здесь:")
print("=" * 50)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x > CANVAS_WIDTH:
                for key, rect in input_boxes.items():
                    if rect.collidepoint(x, y):
                        active_input = key
                        break
                else:
                    active_input = None
                draw_button = pygame.Rect(CANVAS_WIDTH + 50, 350, 180, 40)
                if draw_button.collidepoint(x, y):
                    try:
                        x0 = int(input_values['x0'])
                        y0 = int(input_values['y0'])
                        x1 = int(input_values['x1'])
                        y1 = int(input_values['y1'])
                        if all(-GRID_OFFSET <= coord <= GRID_OFFSET for coord in [x0, y0, x1, y1]):
                            print(f"\nПостроение линии от ({x0},{y0}) до ({x1},{y1}):")
                            print("-" * 30)
                            calculated_points = bresenham_line(x0, y0, x1, y1)
                            line_points = calculated_points
                            print("-" * 30)
                            print(f"Всего точек: {len(calculated_points)}")
                        else:
                            print(f"Ошибка: координаты должны быть в диапазоне -{GRID_OFFSET} до {GRID_OFFSET}")
                    except ValueError:
                        print("Ошибка: введите целые числа")
        if event.type == pygame.KEYDOWN:
            if active_input:
                if event.key == pygame.K_RETURN:
                    active_input = None
                elif event.key == pygame.K_BACKSPACE:
                    input_values[active_input] = input_values[active_input][:-1]
                elif event.unicode.isdigit() or (event.unicode == '-' and not input_values[active_input]):
                    input_values[active_input] += event.unicode
    screen.fill(LIGHT_BG)
    draw_grid()
    draw_line()
    draw_tool_panel()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()