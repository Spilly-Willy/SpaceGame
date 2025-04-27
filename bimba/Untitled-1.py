from pygame import *
from random import randint
from time import *

init()
font.init()

# Константы
WIDTH, HEIGHT = 700, 500
HERO_SIZE = (80, 80)
HERO_SPEED = 5
ENEMY_SIZE = (80, 50)
ENEMY_SPEED = 1
BULLET_SIZE = (25, 35)
BULLET_SPEED = 6
FPS = 60

# Создание окна
wind = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Шутер')

# Загрузка изображений и звуков
background = transform.scale(image.load('galaxy.jpg'), (WIDTH, HEIGHT))
mixer.music.load('space.ogg')
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')

# Создание шрифтов
font1 = font.Font(None, 36)
font2 = font.Font(None, 72)

# Переменные игры
missed = 0
score = 0
max_missed = 3
win_score = 10

class GameSprite(sprite.Sprite):
    def __init__(self, image_path, size, pos, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_path), size)
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed

    def draw(self, win):
        win.blit(self.image, self.rect)

class Hero(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet('bullet.png', BULLET_SIZE, (self.rect.centerx - 5, self.rect.top), BULLET_SPEED)
        bullets.add(bullet)
        fire_sound.play()

    def clicker(self):
        start_time = time.time()
        clicks = 0
        while time.time() - start_time < 10:
            keys = key.get_pressed()
            if keys[K_SPACE]:
                clicks += 1
                print(f"Кликов сделано: {clicks}")
        return clicks >= 30

class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(50, WIDTH - 50)
            self.rect.y = randint(-150, -50)
            missed += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Создание игровых объектов
player = Hero('rocket.png', HERO_SIZE, (300, 400), HERO_SPEED)
enemies = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', ENEMY_SIZE, (randint(50, WIDTH - 50), randint(-150, -50)), randint(1, 2))
    enemies.add(enemy)

# Основной цикл игры
clock = time.Clock()
game = True
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    if game:
        keys = key.get_pressed()
        player.update()
        enemies.update()
        bullets.update()

        wind.blit(background, (0, 0))
        player.draw(wind)
        enemies.draw(wind)
        bullets.draw(wind)

        for bullet in bullets:
            enemy_hit = sprite.spritecollide(bullet, enemies, True)
            if enemy_hit:
                bullet.kill()
                score += len(enemy_hit)
                enemies.add(Enemy('ufo.png', ENEMY_SIZE, (randint(50, WIDTH - 50), randint(-150, -50)), randint(1, 3)))

        if missed >= max_missed or sprite.spritecollide(player, enemies, False):
            game = False
            result_text = "Вы проиграли!"

        if score >= win_score:
            if player.clicker():
                game = False
                result_text = "Вы выиграли!"
            else:
                game = False
                result_text = "Вы проиграли!"

    text_missed = font1.render(f"Пропущено: {missed}", True, (255, 0, 0))
    text_score = font1.render(f"Счёт: {score}", True, (0, 255, 0))
    wind.blit(text_missed, (10, 10))
    wind.blit(text_score, (10, 40))

