import pygame
import sys
import os
import random
import time
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (148, 0, 211)


startSpeed = 3
moveSpeed = startSpeed
maxSpeed = 10
score = 0
eNum = -1
paused = False

textFonts = ['comicsansms', 'arial']
textSize = 48

GAME_ROOT_FOLDER = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(GAME_ROOT_FOLDER, "Images")


def GameOver():
    fontGameOver = pygame.font.SysFont(textFonts, textSize)
    fontGameOver2 = pygame.font.SysFont(textFonts, textSize//2)
    textGameOver = fontGameOver.render("Game Over!", True, RED)
    textGameOver2 = fontGameOver2.render("Score " + str(score), True, RED)
    rectGameOver = textGameOver.get_rect()
    rectGameOver2 = textGameOver2.get_rect()
    rectGameOver.center = (IMG_ROAD.get_width()//2,
                           IMG_ROAD.get_height()//2)
    rectGameOver2.center = (IMG_ROAD.get_width()//2,
                            IMG_ROAD.get_height()//2+80)
    screen.fill(BLACK)
    screen.blit(textGameOver, rectGameOver)
    screen.blit(textGameOver2, rectGameOver2)
    pygame.display.update()
    player.kill()
    enemy.kill()
    time.sleep(5)
    pygame.quit()
    sys.exit()


# 초기화
pygame.init()

clock = pygame.time.Clock()
clock.tick(60)

pygame.display.set_caption("Crazy Driver")

IMG_ROAD = pygame.image.load(os.path.join(IMAGE_FOLDER, "Road.png"))
IMG_PLAYER = pygame.image.load(os.path.join(IMAGE_FOLDER, "Player.png"))
IMG_ENEMIES = []
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy2.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy3.png")))
IMG_ENEMIES.append(pygame.image.load(
    os.path.join(IMAGE_FOLDER, "IceCube.png")))

screen = pygame.display.set_mode(IMG_ROAD.get_size())

h = IMG_ROAD.get_width()//2
v = IMG_ROAD.get_height() - (IMG_PLAYER.get_height()//2)

player = pygame.sprite.Sprite()
player.image = IMG_PLAYER
player.surf = pygame.Surface(IMG_PLAYER.get_size())
player.rect = player.surf.get_rect(center=(h, v))

while True:
    pygame.display.set_caption("Crazy Driver - Score " + str(score))

    screen.blit(IMG_ROAD, (0, 0))

    screen.blit(player.image, player.rect)

    if eNum == -1:
        eNum = random.randrange(0, len(IMG_ENEMIES))
        hl = IMG_ENEMIES[eNum].get_width()//2
        hr = IMG_ROAD.get_width() - (IMG_ENEMIES[eNum].get_width()//2)
        h = random.randrange(hl, hr)
        v = 0

        enemy = pygame.sprite.Sprite()
        enemy.image = IMG_ENEMIES[eNum]
        enemy.surf = pygame.Surface(IMG_ENEMIES[eNum].get_size())
        enemy.rect = enemy.surf.get_rect(center=(h, v))

    keys = pygame.key.get_pressed()

    if paused:
        if not keys[K_SPACE]:
            moveSpeed = tempSpeed
            paused = False
    else:
        if (keys[K_LEFT] or keys[K_a]) and player.rect.left > 0:
            player.rect.move_ip(-moveSpeed, 0)
            if player.rect.left < 0:
                player.rect.left = 0
        if (keys[K_RIGHT] or keys[K_d]) and player.rect.right < IMG_ROAD.get_width():
            player.rect.move_ip(moveSpeed, 0)
            if player.rect.right > IMG_ROAD.get_width():
                player.rect.right = IMG_ROAD.get_width()
        if keys[K_SPACE]:
            tempSpeed = moveSpeed
            moveSpeed = 0
            paused = True

    screen.blit(enemy.image, enemy.rect)

    enemy.rect.move_ip(0, moveSpeed)

    if (enemy.rect.bottom > IMG_ROAD.get_height()):
        enemy.kill()
        eNum = -1
        score += 1
        moveSpeed += 1

        # if moveSpeed < maxSpeed:
        #    moveSpeed += 1

    if eNum >= 0 and pygame.sprite.collide_rect(player, enemy):
        if eNum == 3:
            moveSpeed = startSpeed
        else:
            GameOver()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
