import pygame
from random import randrange

WIDTH = 12
HEIGHT = 15
CELL_SIZE = 50
TOP_BAR = 75
WIDTH_SIZE = WIDTH * CELL_SIZE
HEIGHT_SIZE = (HEIGHT * CELL_SIZE) + TOP_BAR

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (105,105,105)
BLACK = (0, 0, 0)

BACKGROUND = BLACK

BODY = 1
FRUIT = 4

def draw_text(surface, text, size, x, y, color):
    font = pygame.font.SysFont("calibri", size, bold=True)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def generate_red_dot():
    x = randrange(HEIGHT)
    y = randrange(WIDTH)
    while mat[x][y] != 0:
        x = randrange(HEIGHT)
        y = randrange(WIDTH)
    mat[x][y] = FRUIT

def print_dot(num, h, w):
    if num == BODY:
        color = GREEN
    elif num == FRUIT:
        color = RED
    pygame.draw.rect(screen, color, (w * CELL_SIZE, (h * CELL_SIZE) + TOP_BAR, CELL_SIZE, CELL_SIZE))

def move_snake(movement, score):
    if movement is None:
        return False, score
    
    head = [snake[0][0], snake[0][1]]
    
    if movement == "UP":
        head[0] -= 1
    if movement == "DOWN":
        head[0] += 1
    if movement == "LEFT":
        head[1] -= 1
    if movement == "RIGHT":
        head[1] += 1
    
    if head[0] < 0 or head[0] > HEIGHT-1:
        return True, score
    if head[1] < 0 or head[1] > WIDTH-1:
        return True, score

    tail = snake[len(snake)-1]

    snake.insert(0, head)
    if mat[head[0]][head[1]] != FRUIT:
        snake.pop(len(snake)-1)
    
    if mat[head[0]][head[1]] == FRUIT:
        generate_red_dot()
        score += 100
    if mat[head[0]][head[1]] == BODY:
        return True, score

    mat[head[0]][head[1]] = BODY
    mat[tail[0]][tail[1]] = 0
    return False, score

def game_over_message():
    draw_text(screen, "GAME OVER", 20, WIDTH_SIZE//4 * 3 , TOP_BAR//4 , BLACK)
    draw_text(screen, "Press SPACE to play again", 20, WIDTH_SIZE//4 * 3 , TOP_BAR//4*3 , BLACK)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                waiting = False
                return False

def draw_lateral_bar():
    pygame.draw.rect(screen, GREY, (0, 0, WIDTH_SIZE, TOP_BAR))
    draw_text(screen, "SCORE: {}".format(score), 14, 50 + TOP_BAR//2 , TOP_BAR//2 , BLACK)

def display_frame():
    screen.fill(BACKGROUND)
    for h in range(len(mat)):
        for w in range(len(mat[0])):
            if mat[h][w] != 0:
                print_dot(mat[h][w], h, w)
    draw_lateral_bar()
    pygame.display.flip()

pygame.init()
screen = pygame.display.set_mode((WIDTH_SIZE, HEIGHT_SIZE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
running = True
movement = None
last_movement = None

score = 0
game_over = False

snake = []
snake.append([HEIGHT//2, WIDTH//2])

mat = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
mat[snake[0][0]][snake[0][1]] = BODY
generate_red_dot()

while running:
    clock.tick(5)
    display_frame()
    if game_over:
        game_over = game_over_message()
        if game_over:
            break
        else:
            score = 0
            mat = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
            generate_red_dot()
            snake = []
            snake.append([HEIGHT//2, WIDTH//2])
            mat[snake[0][0]][snake[0][1]] = BODY
            movement = None
            last_movement = None
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and last_movement != "DOWN":
                movement = "UP"
            if event.key == pygame.K_DOWN and last_movement != "UP":
                movement = "DOWN"
            if event.key == pygame.K_LEFT and last_movement != "RIGHT":
                movement = "LEFT"
            if event.key == pygame.K_RIGHT and last_movement != "LEFT":
                movement = "RIGHT"
        if event.type == pygame.QUIT:
            running = False
    last_movement = movement 
    game_over, score = move_snake(movement, score)

pygame.quit()