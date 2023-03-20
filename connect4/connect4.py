import pygame

CELL_SIZE = 100
WIDTH = 7 * CELL_SIZE
HEIGHT = 6 * CELL_SIZE

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BACKGROUND = (50, 98, 168)

def manage_event(event):
    if event.type == pygame.QUIT:
        return False
    
    return True

def display_frame():
    screen.fill(BACKGROUND)
    print_table()
    pygame.display.flip()

def print_table():
    cell = CELL_SIZE // 2
    count = 0
    for i in range(6):
        for j in range(7):
            count += 1
            if mat[i][j] == 0:
                pygame.draw.circle(screen, WHITE, (cell + cell*j*2, cell + cell*i*2), CELL_SIZE // 3, width=0)
    pass

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")
clock = pygame.time.Clock()

mat = [[0 for _ in range(7)] for _ in range(6)]
print(mat)

game_over = False
running = True
winner = 0
turn = 0

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        running = manage_event(event)
    
    display_frame()

pygame.quit()