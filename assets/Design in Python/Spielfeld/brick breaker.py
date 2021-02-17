import pygame
from pygame.locals import *
from pygame.sprite import *
import random
from playsound import playsound

pygame.init()
# Display configuration
pygame.display.set_caption('Stone Crusher')
screen = pygame.display.set_mode((1280, 720))

icon = pygame.image.load('images/icon.ico')
pygame.display.set_icon(icon)

# pygame.mixer.init()
# pygame.mixer.music.load('')
# pygame.mixer.music.play(-1)


# Entities
background = pygame.image.load('images/playfield.png')
life = pygame.image.load('images/heart.png')
bar = pygame.image.load('images/bar.png')

while True:

    screen.blit(background, (0, 0))
    screen.blit(life, (458, 5))
    screen.blit(life, (520, 5))
    screen.blit(life, (581, 5))
    screen.blit(life, (643, 5))
    screen.blit(life, (706, 5))
    screen.blit(life, (771, 5))
    screen.blit(bar, (0, 58))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        pygame.display.flip()
