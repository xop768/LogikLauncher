from pygame import *
from random import randint
import sounddevice as sd
import numpy as np

fs = 15000
chunk = 256
mic_level = 0.0

def audio_callback(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

init()
window_size = 1200, 800
window = display.set_mode(window_size)
clock = time.Clock()

player_rect = Rect(150, window_size[1]//2-100,
                   100, 100)

def generate_pipes(count, pipe_width=140,
                   gap=280, min_height=50,
                   max_height=440, distance=650):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0, pipe_width, height)
        bottom_pipe = Rect(start_x, height+gap,
                           pipe_width,
                           window_size[1]-(height+gap))
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes

game_pipes = generate_pipes(150)

main_font = font.Font(None, 100)
score = 0
lose = False
running = True
wait = 40
y_vel = 0.0
gravity = 0.6

THRESH = 0.001
IMPULSE = -8.0

with sd.InputStream(samplerate=fs, channels=1,
                    blocksize=chunk,
                    callback=audio_callback):
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        
        if mic_level > THRESH:
            y_vel = IMPULSE
        y_vel += gravity
        player_rect.y += int(y_vel)
        
        window.fill('sky blue')
        draw.rect(window, 'red', player_rect)
        for pipe in game_pipes[:]:
            if lose != True:
                pipe.x -= 10
            draw.rect(window, 'green', pipe)
            if pipe.x <= -100:
                game_pipes.remove(pipe)
                score += 0.5
            if player_rect.colliderect(pipe):
                lose = True
        if len(game_pipes) < 8:
            game_pipes += generate_pipes(150)
        
        score_text = main_font.render(f'{int(score)}', 1, 'black')
        center_text = window_size[0]//2-score_text.get_rect().w//2
        window.blit(score_text, (center_text, 40))
        
        keys = key.get_pressed()
        '''if keys[K_UP] and not lose:
            player_rect.y -= 15
        if keys[K_DOWN] and not lose:
            player_rect.y += 15'''
        
        if keys[K_r] and lose:
            lose = False
            score = 0
            game_pipes = generate_pipes(150)
            player_rect.y = window_size[1]//2-100
            y_vel = 0.0
        
        if player_rect.bottom > window_size[1]:
            player_rect.bottom = window_size[1]
            y_vel = 0.0
        if player_rect.top < 0:
            player_rect.top = 0
            if y_vel < 0:
                y_vel = 0.0
        
        if lose and wait > 1:
            for pipe in game_pipes:
                pipe.x += 8
            wait -= 1
        else:
            lose = False
            wait = 40
        
        display.update()
        clock.tick(60)

    quit()
