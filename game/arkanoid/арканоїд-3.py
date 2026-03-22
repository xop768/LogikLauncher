import pygame
import sys

pygame.init()

clock = pygame.time.Clock()

mw = pygame.display.set_mode(size = (500,500))
back = (200,255,255)
mw.fill(back)
pygame.display.set_caption(title = 'Арканоїд')

game = True

class Area():
    def __init__(self, x = 0, y = 0, width = 10, height = 10,
                 color = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    def colliderect(self, rect):
        return self.rect.colliderect(rect)
class Picture(Area):
    def __init__(self, filename, x = 0, y = 0, width = 10,
                 height = 10):
        Area.__init__(self, x, y, width, height, color = None)
        self.image = pygame.image.load(filename)
    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))
class Label(Area):
    def set_text(self, text, fsize, text_color = (0,0,0)):
        self.image = pygame.font.SysFont('Verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x, shift_y):
        mw.blit(self.image, (self.rect.x+shift_x,self.rect.y+shift_y))

move_right = False
move_left = False

ball = Picture('ball.png', 160, 200, 50, 50)
racket_x = 200
racket_y = 300
platform = Picture('platform.png', racket_x, racket_y, 100, 30)

start_x = 5
start_y = 5
count = 2 # Кількість монстрів у ряді
monsters = []
for i in range(3):
    x = start_x + 27.5 * i
    y = start_y + 55 * i
    for j in range(count):
        m = Picture('enemy.png', x, y, 50, 50)
        monsters.append(m)
        x += 55
    count -= 1

dx = 3
dy = 3

while game == True:
    mw.fill(back)
    ball.fill()
    ball.draw()
    platform.fill()
    platform.draw()
    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect) == True:
            monsters.remove(m)
            m.fill()
            dy *= -1
    ball.rect.x += dx
    ball.rect.y += dy
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1
    if ball.rect.y < 0:
        dy *= -1
    if ball.colliderect(platform.rect) == True:
        dy *= -1
    if ball.rect.y > 450:
        message = Label(100, 150, 50, 50, back)
        message.set_text('YOU LOSE!', 60, (255,0,0))
        message.draw(10, 10)
        game = False
        
    if len(monsters) == 0:
        message = Label(100, 150, 50, 50, back)
        message.set_text('YOU WIN!', 60, (0,255,0))
        message.draw(10, 10)
        game = False
        
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False
        if event.type == pygame.QUIT:
            game = False
            pygame.quit()
            sys.exit()
    if move_right == True:
        platform.rect.x += 3
    if move_left == True:
        platform.rect.x -= 3
    pygame.display.update()
    clock.tick(60)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
