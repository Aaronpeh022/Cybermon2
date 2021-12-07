# imports
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# constants
WIN_WIDTH = 640
WIN_HEIGHT = 480

pygame.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = True

screen.fill((255, 255, 255))

surf = pygame.Surface((50, 50))

surf.fill((0, 0, 0))
rect = surf.get_rect()

screen.blit(surf, (WIN_WIDTH / 2, WIN_HEIGHT / 2))
pygame.display.flip()
