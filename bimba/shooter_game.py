from pygame import *
from random import randint
import time as t

init()
font.init()

Width, Height = 700, 500
Hero_size = (80, 80)
Hero_speed = 5
Enemy_size = (80, 50)
Enemy_speed = 1
Bullet_size = (25, 35)
Bullet_speed = 6
FPS = 60

wind = display.set_mode([Width, Height])
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (Width, Height))

fire_sound = mixer.Sound('fire.ogg')

font1 = font.Font(None, 36)
font2 = font.Font(None, 72)

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
        if keys[K_RIGHT] and self.rect.x < Width - self.rect.width:
            self.rect.x += self.speed
    global keys

    def shoot(self):
        bullet = Bullet('bullet.png', Bullet_size, (self.rect.centerx - 5, self.rect.top), Bullet_speed)
        bullets.add(bullet)
        fire_sound.play()

class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > Height:
            self.rect.x = randint(50, Width - 50)
            self.rect.y = randint(-150, -50)
            missed += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Meteorite(GameSprite):
    def __init__(self, image_path, size, pos, speed):
        super().__init__(image_path, size, pos, speed)
        self.rect.y = randint(-100, -50)

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > Height:
            self.kill()

def create_meteorites():
    for i in range(2):
        for i in range(2):
            meteorite = Meteorite('meteor.png', (50, 50), (randint(0, Width), randint(-100, -50)), randint(2, 5))
            meteorites.add(meteorite)


player = Hero('rocket.png', Hero_size, (300, 400), Hero_speed)
enemies = sprite.Group()
bullets = sprite.Group()
meteorites = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', Enemy_size, (randint(50, Width - 50), randint(-150, -50)), randint(1, 2))
    enemies.add(enemy)
create_meteorites()

clock = time.Clock()
Game = True
running = True
result_text = ""
cd = 0

mixer.music.load('space.mp3')
mixer.music.play(-1)

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    if Game:

        keys = key.get_pressed()
        cd += 1
        if keys[K_SPACE] and cd >= 20:
            player.shoot()
            cd = 0

        player.update()
        enemies.update()
        bullets.update()
        meteorites.update()
        
        wind.blit(background, (0, 0))
        meteorites.draw(wind)
        player.draw(wind)
        enemies.draw(wind)
        bullets.draw(wind)

        for bullet in bullets:
            enemy_hit = sprite.spritecollide(bullet, enemies, True)
            if enemy_hit:
                bullet.kill()
                boom = mixer.Sound('explorer.mp3')
                boom.play()
                score += len(enemy_hit)
                enemies.add(Enemy('ufo.png', Enemy_size, (randint(50, Width - 50), randint(-150, -50)), randint(1, 3)))
        
        if missed >= max_missed or sprite.spritecollide(player, enemies, False):
            Game = False
            result_text = "Вы проиграли!"
        
        if score >= win_score:
            Game = False
            result_text = "Вы выиграли!"
            pobeda = mixer.Sound('game-won.mp3')
            pobeda.play()
    
    text_missed = font1.render(f"Пропущено: {missed}", True, (255, 0, 0))
    text_score = font1.render(f"Счёт: {score}", True, (0, 255, 0))
    wind.blit(text_missed, (10, 10))
    wind.blit(text_score, (10, 40))
    
    if not Game:
        text_result = font2.render(result_text, True, (255, 255, 255))
        wind.blit(text_result, (Width // 2 - text_result.get_width() // 2, Height // 2 - text_result.get_height() // 2))
    
    display.update()
    clock.tick(60)    
   
quit()
