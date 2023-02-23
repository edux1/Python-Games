import pygame, sys

pygame.init()

size = (500, 500)

screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            sys.exit()