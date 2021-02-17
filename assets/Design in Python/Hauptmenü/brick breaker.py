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
background = pygame.image.load('images/mainMenu.png')
Scoreboard_Button = pygame.image.load('images/Scoreboard_Button.png')
Play_Button = pygame.image.load('images/Play_Button.png')
Setting_Button = pygame.image.load('images/Setting_Button.png')

while True:

    screen.blit(background, (0, 0))
    screen.blit(Scoreboard_Button, (402, 282))
    screen.blit(Play_Button, (575, 282))
    screen.blit(Setting_Button, (748, 282))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        pygame.display.flip()
