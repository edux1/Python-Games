import pygame, sys

pygame.init()

# COLORES
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BACKGROUND = (51, 181, 255)

size = (500, 500)

screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BACKGROUND)
    ###-----------------
    for i in range(0, 501, 25):
        pygame.draw.line(screen, WHITE, (i, 0), (i, 500), 3)
        pygame.draw.line(screen, WHITE, (0, i), (500, i), 3)

    ###-----------------

    pygame.display.flip()