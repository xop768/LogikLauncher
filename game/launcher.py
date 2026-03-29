import pygame
import subprocess
import sys
import os

# ВСТАНОВЛЮЄМО ШЛЯХ ДО ПАПКИ З ІГРАМИ
# Використовуємо r"" (raw string), щоб Windows правильно сприймав зворотні слеші
BASE_DIR = r"C:\Users\Logika\Desktop\LogikLauncher-main\game"

pygame.init()

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мій Ігровий Хаб")

clock = pygame.time.Clock()

# Кольори
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
COLORS = {
    "blue": (70, 130, 180),
    "green": (60, 179, 113),
    "orange": (255, 140, 0),
    "red": (200, 50, 50)
}

font_title = pygame.font.SysFont('Verdana', 50, bold=True)
font_btn = pygame.font.SysFont('Verdana', 22)

# Список ігор (шляхи відносно папки BASE_DIR)
games_list = [
    ("Пінг-Понг (Онлайн)", "ping-pong/client.py", COLORS["blue"]),
    ("Flappy Bird (Класика)", "Flappybird/Flappy Bird (base).py", COLORS["orange"]),
    ("Арканоїд", "arkanoid/арканоїд-3.py", COLORS["red"])
]

def draw_button(text, rect, color, is_hovered):
    draw_color = tuple(min(c + 40, 255) for c in color) if is_hovered else color
    pygame.draw.rect(screen, draw_color, rect, border_radius=12)
    pygame.draw.rect(screen, WHITE, rect, width=2, border_radius=12)

    txt_surface = font_btn.render(text, True, WHITE)
    txt_rect = txt_surface.get_rect(center=rect.center)
    screen.blit(txt_surface, txt_rect)

def run_game(file_name):
    # Тепер file_path будується відносно C:\Users\Logika\Desktop\LogikLauncher-main\game
    file_path = os.path.normpath(os.path.join(BASE_DIR, file_name))
    game_folder = os.path.dirname(file_path) # Папка конкретної гри

    if not os.path.exists(file_path):
        print(f"Помилка: Файл не знайдено за шляхом: {file_path}")
        return

    try:
        # ✅ Спеціальна логіка для Пінг-Понга (запуск сервера)
        if "ping-pong/client.py" in file_name:
            server_path = os.path.join(game_folder, "server.py")
            if os.path.exists(server_path):
                print("Запуск сервера...")
                subprocess.Popen([sys.executable, server_path], cwd=game_folder)

        print(f"Запуск гри: {file_name}")
        # Запускаємо гру, вказуючи її власну папку як робочу (cwd)
        subprocess.Popen([sys.executable, file_path], cwd=game_folder)

    except Exception as e:
        print(f"Помилка запуску: {e}")

# Створення кнопок
button_rects = []
for i in range(len(games_list)):
    rect = pygame.Rect(WIDTH//2 - 160, 130 + i * 80, 320, 60)
    button_rects.append(rect)

# Головний цикл
running = True
while running:
    screen.fill(BLACK)

    title = font_title.render("GAME HUB", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 70)))

    mouse_pos = pygame.mouse.get_pos()

    for i, (name, file, color) in enumerate(games_list):
        rect = button_rects[i]
        is_hover = rect.collidepoint(mouse_pos)
        draw_button(name, rect, color, is_hover)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        run_game(games_list[i][1])

    pygame.display.update()
    clock.tick(60)

pygame.quit()
