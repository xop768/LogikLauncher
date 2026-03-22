from pygame import *
import socket
import json
from threading import Thread

WIDTH, HEIGHT = 800, 600

init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Пінг-Понг")

font_big = font.Font(None, 72)
font_main = font.Font(None, 36)

def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('localhost', 8080))

            buffer = ""
            game_state = {}

            my_id = int(client.recv(24).decode())
            return my_id, game_state, buffer, client
        except:
            pass

def receive():
    global buffer, game_state, game_over
    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data

            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
        except:
            game_state["winner"] = -1
            break

# --- МЕНЮ ---
def menu():
    while True:
        screen.fill((0, 0, 0))

        title = font_big.render("PONG", True, (255,255,255))
        screen.blit(title, title.get_rect(center=(WIDTH//2, 150)))

        btn_bot = Rect(WIDTH//2 - 150, 300, 300, 60)
        draw.rect(screen, (0, 200, 0), btn_bot)

        text_bot = font_main.render("Грати з ботом", True, (0,0,0))
        screen.blit(text_bot, text_bot.get_rect(center=btn_bot.center))

        for e in event.get():
            if e.type == QUIT:
                exit()
            if e.type == MOUSEBUTTONDOWN:
                if btn_bot.collidepoint(mouse.get_pos()):
                    return

        display.update()
        clock.tick(60)

# запуск меню
menu()

game_over = False
winner = None
you_winner = None

my_id, game_state, buffer, client = connect_to_server()
Thread(target=receive, daemon=True).start()

while True:
    for e in event.get():
        if e.type == QUIT:
            exit()

    if "countdown" in game_state and game_state["countdown"] > 0:
        screen.fill((0, 0, 0))
        text = font_big.render(str(game_state["countdown"]), True, (255,255,255))
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        display.update()
        continue

    if "winner" in game_state and game_state["winner"] is not None:
        screen.fill((20,20,20))

        if you_winner is None:
            you_winner = (game_state["winner"] == my_id)

        text = "Ти переміг!" if you_winner else "Ти програв"
        win = font_big.render(text, True, (255,215,0))
        screen.blit(win, win.get_rect(center=(WIDTH//2, HEIGHT//2)))

        display.update()
        continue

    if game_state:
        screen.fill((30,30,30))

        draw.rect(screen,(0,255,0),(20, game_state['paddles']['0'],20,100))
        draw.rect(screen,(255,0,255),(WIDTH-40, game_state['paddles']['1'],20,100))

        draw.circle(screen,(255,255,255),
                    (game_state['ball']['x'], game_state['ball']['y']),10)

        score = font_main.render(
            f"{game_state['scores'][0]} : {game_state['scores'][1]}",
            True,(255,255,255))
        screen.blit(score,(WIDTH//2-30,20))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_w]:
        client.send(b"UP")
    elif keys[K_s]:
        client.send(b"DOWN")