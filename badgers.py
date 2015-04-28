import pygame
import math
import random
from pygame.locals import *


class Plot(object):
    X = 1
    Y = 2
    left = 0
    top = 1


class Key(object):
    W = 0
    A = 1
    S = 2
    D = 3


def radians(pos):
    return 360 - pos * 57.29


def calculate_accuracy():
    if accuracy['shots'] != 0:
        return accuracy['hits'] * 1.0 / accuracy['shots'] * 100
    else:
        return 0



#  2
pygame.init()
screen_right = 640
screen_bottom = -64
screen_top = 480
screen_left = -64
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [100, 100]
accuracy = {'hits': 0, 'shots': 0}
arrows = []
badtimer = 100
badtimer1 = 0
badguys = [[screen_top, 100]]
healthvalue = 194
pygame.mixer.init()
seconds = 90
game_time = seconds * 1000

#  3
player = pygame.image.load('resources/images/dude.png')
grass = pygame.image.load('resources/images/grass.png')
castle = pygame.image.load('resources/images/castle.png')
arrow = pygame.image.load('resources/images/bullet.png')
badguyimg1 = pygame.image.load('resources/images/badguy.png')
badguyimg = badguyimg1
healthbar = pygame.image.load('resources/images/healthbar.png')
health = pygame.image.load('resources/images/health.png')
gameover = pygame.image.load('resources/images/gameover.png')
youwin = pygame.image.load('resources/images/youwin.png')

#  3.1 sound
hit = pygame.mixer.Sound('resources/audio/explode.wav')
enemy = pygame.mixer.Sound('resources/audio/enemy.wav')
shoot = pygame.mixer.Sound('resources/audio/shoot.wav')
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

#  4
running = True
exitcode = ''
while running:
    badtimer -= 1
    #  5 clear screen
    screen.fill(0)

    #  6 draw screen elements
    for x in range(width/grass.get_width()+1):
        for y in range(height/grass.get_height()+1):
            screen.blit(grass, (x*100, y*100))
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    #   6.1 player angle and position
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
    playerrot = pygame.transform.rotate(player, radians(angle))
    playerpos1 = (playerpos[Plot.left] - playerrot.get_rect().width / 2, playerpos[Plot.top] - playerrot.get_rect().height / 2)
    screen.blit(playerrot, playerpos1)

    #  6.2 draw arrows
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[Plot.X] += velx
        bullet[Plot.Y] += vely
        if bullet[Plot.X] < screen_left or bullet[Plot.X] > screen_right or bullet[Plot.Y] < screen_bottom or bullet[Plot.Y] > screen_top:
            arrows.pop(index)

        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, radians(projectile[Plot.left]))
            screen.blit(arrow1, (projectile[Plot.X], projectile[Plot.Y]))

    #  6.3 draw badgers
    if badtimer == 0:
        badguys.append([screen_right, random.randint(50, 430)])
        badtimer = 100 - (badtimer1 * 2)
        if badtimer1 > 35:
            badtimer1 = 35
        else:
            badtimer1 += 5
    index = 0
    for badguy in badguys:
        if badguy[Plot.left] < screen_left:
            badguys.pop(index)
        badguy[Plot.left] -= 7

        #  6.3.1 attack castle
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[Plot.top]
        badrect.left = badguy[Plot.left]
        if badrect.left < 64:
            hit.play()
            healthvalue -= random.randint(5, 20)
            badguys.pop(index)

        #  6.3.2 collisions
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[Plot.X]
            bullrect.top = bullet[Plot.Y]
            if badrect.colliderect(bullrect):
                enemy.play()
                accuracy['hits'] += 1
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1

        #  6.3.3 next bad guy
        index += 1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    #  6.4 draw clock
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(
        '{}:{}'.format(
            str((game_time - pygame.time.get_ticks()) / 60000),
            str((game_time - pygame.time.get_ticks()) / 1000 % 60).zfill(2),
        ), True, (0, 0, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)

    #  6.4 health bar
    screen.blit(healthbar, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1 + 8, 8))

    #  7
    pygame.display.flip()

    #  8
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[Key.W] = True
            elif event.key == K_a:
                keys[Key.A] = True
            elif event.key == K_s:
                keys[Key.S] = True
            elif event.key == K_d:
                keys[Key.D] = True

        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[Key.W] = False
            elif event.key == K_a:
                keys[Key.A] = False
            elif event.key == K_s:
                keys[Key.S] = False
            elif event.key == K_d:
                keys[Key.D] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            accuracy['shots'] += 1

            arrows.append([math.atan2(
                position[Plot.top] - (playerpos1[Plot.top] + 32),
                position[Plot.left] - (playerpos1[Plot.left] + 26)),
                playerpos1[Plot.left] + 32,
                playerpos1[Plot.top] + 32
            ])

    #  9  movement keys
    #  TODO bounds check.  Keep rabbit on screen.
    if keys[Key.W]:
        playerpos[Plot.top] -= 5
    elif keys[Key.S]:
        playerpos[Plot.top] += 5
    elif keys[Key.A]:
        playerpos[Plot.left] -= 5
    elif keys[Key.D]:
        playerpos[Plot.left] += 5

    #  10 win/lose check
    if pygame.time.get_ticks() >= game_time:
        running = False
        exitcode = 'win'
    if healthvalue <= 0:
        running = False
        exitcode = 'lose'

    #  11 win/lose display
    if exitcode:
        if exitcode == 'lose':
            screen.blit(gameover, (0, 0))
            pos = (255, 0, 0)
        elif exitcode == 'win':
            screen.blit(youwin, (0, 0))
            pos = (0, 255, 0)
        pygame.font.init()
        font = pygame.font.Font(None, 24)
        text = font.render("Accuracy: {}%".format(calculate_accuracy()), True, pos)
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery + 24
        screen.blit(text, textRect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
            pygame.display.flip()
