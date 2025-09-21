import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 1000, 700
CANVAS_WIDTH = 700
GRID_SIZE = 20
GRID_WIDTH = CANVAS_WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
DARK_BG = (255, 255, 255)
LIGHT_TEXT = (0, 0, 0)
ACCENT = (100, 180, 255)
HIGHLIGHT = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 89, 94)
GREEN = (138, 201, 38)
BLUE = (25, 130, 196)
YELLOW = (255, 202, 58)
PURPLE = (187, 107, 217)
ORANGE = (255, 158, 74)
CYAN = (0, 188, 212)
COLORS = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN, WHITE]
COLOR_NAMES = ["Черный", "Красный", "Зеленый", "Синий", "Желтый", "Фиолетовый", "Оранжевый", "Бирюзовый", "Белый"]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎨 Заливочка")

try:
    title_font = pygame.font.SysFont("arial", 32)
    header_font = pygame.font.SysFont("arial", 24)
    text_font = pygame.font.SysFont("arial", 18)
except:
    title_font = pygame.font.Font(None, 32)
    header_font = pygame.font.Font(None, 24)
    text_font = pygame.font.Font(None, 18)

grid = [[WHITE for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_color = BLACK
draw_mode = True

UI_ELEMENTS = {
    'title': (CANVAS_WIDTH + 20, 20),
    'divider_start': (CANVAS_WIDTH + 20, 70),
    'divider_end': (WIDTH - 20, 70),
    'modes_header': (CANVAS_WIDTH + 20, 90),
    'draw_button': (CANVAS_WIDTH + 30, 130),
    'fill_button': (CANVAS_WIDTH + 30, 190),
    'colors_header': (CANVAS_WIDTH + 20, 250),
    'instructions_header': (CANVAS_WIDTH + 20, 520),
    'instructions_start': (CANVAS_WIDTH + 30, 560)
}

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, grid[y][x], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


def draw_tool_panel():
    panel_rect = pygame.Rect(CANVAS_WIDTH, 0, WIDTH - CANVAS_WIDTH, HEIGHT)
    pygame.draw.rect(screen, (240, 240, 240), panel_rect)
    pygame.draw.line(screen, ACCENT, (CANVAS_WIDTH, 0), (CANVAS_WIDTH, HEIGHT), 2)
    title = title_font.render("Paint =)", True, ACCENT)
    screen.blit(title, UI_ELEMENTS['title'])
    pygame.draw.line(screen, ACCENT, UI_ELEMENTS['divider_start'], UI_ELEMENTS['divider_end'], 1)
    header = header_font.render("Режимы работы:", True, LIGHT_TEXT)
    screen.blit(header, UI_ELEMENTS['modes_header'])
    draw_rect = pygame.Rect(UI_ELEMENTS['draw_button'][0], UI_ELEMENTS['draw_button'][1], 200, 40)
    color = ACCENT if draw_mode else (200, 200, 200)
    pygame.draw.rect(screen, color, draw_rect, border_radius=8)
    pygame.draw.rect(screen, ACCENT, draw_rect, 2, border_radius=8)
    draw_text = text_font.render("Рисую", True, BLACK)
    screen.blit(draw_text, (UI_ELEMENTS['draw_button'][0] + 20, UI_ELEMENTS['draw_button'][1] + 12))
    fill_rect = pygame.Rect(UI_ELEMENTS['fill_button'][0], UI_ELEMENTS['fill_button'][1], 200, 40)
    color = ACCENT if not draw_mode else (200, 200, 200)
    pygame.draw.rect(screen, color, fill_rect, border_radius=8)
    pygame.draw.rect(screen, ACCENT, fill_rect, 2, border_radius=8)
    fill_text = text_font.render("Закрашиваю", True, BLACK)
    screen.blit(fill_text, (UI_ELEMENTS['fill_button'][0] + 20, UI_ELEMENTS['fill_button'][1] + 12))
    header = header_font.render("Цвета:", True, LIGHT_TEXT)
    screen.blit(header, UI_ELEMENTS['colors_header'])
    y_offset = UI_ELEMENTS['colors_header'][1] + 40
    for i, (color, name) in enumerate(zip(COLORS, COLOR_NAMES)):
        row = i // 2
        col = i % 2
        color_rect = pygame.Rect(CANVAS_WIDTH + 30 + col * 120, y_offset + row * 50, 100, 40)
        if color == current_color:
            pygame.draw.rect(screen, ACCENT, color_rect, 3, border_radius=6)
        pygame.draw.rect(screen, color, pygame.Rect(color_rect.x + 5, color_rect.y + 5, 30, 30))
        name_text = text_font.render(name, True, BLACK)
        screen.blit(name_text, (color_rect.x + 45, color_rect.y + 12))
    header = header_font.render("Инструкция:", True, LIGHT_TEXT)
    screen.blit(header, UI_ELEMENTS['instructions_header'])
    instructions = [
        "• Выберите режим работы",
        "• Выберите цвет",
        "• Теперь вы можете создать контур",
        "• Переключиться на заливку",
        "• Закрасить контур кликом"
    ]
    y_offset = UI_ELEMENTS['instructions_start'][1]
    for instruction in instructions:
        inst_text = text_font.render(instruction, True, BLACK)
        screen.blit(inst_text, (UI_ELEMENTS['instructions_start'][0], y_offset))
        y_offset += 25

def flood_fill(x, y, target_color, replacement_color):
    if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
        return
    if grid[y][x] != target_color or grid[y][x] == replacement_color:
        return
    grid[y][x] = replacement_color
    flood_fill(x + 1, y, target_color, replacement_color)
    flood_fill(x - 1, y, target_color, replacement_color)
    flood_fill(x, y + 1, target_color, replacement_color)
    flood_fill(x, y - 1, target_color, replacement_color)

def is_click_in_button(pos, button_pos, width=200, height=40):
    x, y = pos
    btn_x, btn_y = button_pos
    return (btn_x <= x <= btn_x + width and
            btn_y <= y <= btn_y + height)

def get_clicked_color(pos):
    x, y = pos
    colors_start_y = UI_ELEMENTS['colors_header'][1] + 40
    for i in range(len(COLORS)):
        row = i // 2
        col = i % 2
        color_rect = pygame.Rect(CANVAS_WIDTH + 30 + col * 120, colors_start_y + row * 50, 100, 40)
        if color_rect.collidepoint(x, y):
            return COLORS[i]
    return None

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x > CANVAS_WIDTH:
                if is_click_in_button((x, y), UI_ELEMENTS['draw_button']):
                    draw_mode = True
                elif is_click_in_button((x, y), UI_ELEMENTS['fill_button']):
                    draw_mode = False
                clicked_color = get_clicked_color((x, y))
                if clicked_color is not None:
                    current_color = clicked_color
            elif x < CANVAS_WIDTH:
                grid_x, grid_y = x // GRID_SIZE, y // GRID_SIZE
                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    if draw_mode:
                        grid[grid_y][grid_x] = current_color
                    else:
                        target_color = grid[grid_y][grid_x]
                        if target_color != current_color:
                            flood_fill(grid_x, grid_y, target_color, current_color)
    screen.fill(WHITE)
    canvas_bg = pygame.Rect(0, 0, CANVAS_WIDTH, HEIGHT)
    pygame.draw.rect(screen, WHITE, canvas_bg)
    draw_grid()
    draw_tool_panel()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()