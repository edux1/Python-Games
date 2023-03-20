import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BACKGROUND = (50, 137, 168)
TEXT_BACKGROUND = (50, 133, 168)
DETAILS_COLOR = (31, 89, 110)
PLAYER1 = (178, 220, 237)
PLAYER2 = (55, 55, 55)

TEXT_SPACE = 100
WIDTH = 600
HEIGHT = 600 + TEXT_SPACE

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("calibri", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def game_over_message(winner):
    # Dibujar zona texto
    text_zone = pygame.Rect(0, 0, WIDTH, TEXT_SPACE)
    pygame.draw.rect(screen, DETAILS_COLOR, text_zone, width=0)

    if winner == 0:
        text = "It's a draw"
    else:
        text = "Player {} won".format(winner)
    draw_text(screen, text, TEXT_SPACE // 2, WIDTH // 2, TEXT_SPACE // 2)
    draw_text(screen, "Press SPACE to play again", TEXT_SPACE // 5, WIDTH // 2, TEXT_SPACE * 4/5)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                waiting = False
                return False
            
def check_win(x, y, player, mat):
    count = 0
    
    w = WIDTH // 6
    h = (HEIGHT - TEXT_SPACE) // 6

    # Vertical check
    for i in range(3):
        if mat[x][i] == player:
            count += 1
    if count == 3:
        return True
    else:
        count = 0
    # Horizontal check
    for j in range(3):
        if mat[j][y] == player:
            count += 1
    if count == 3:
        return True
    else:
        count = 0
    # Diagonal check
    if (x == 0 and y == 0) or (x == 2 and y == 2) or (x == 1 and y == 1):
        for i in range(3):
            if mat[i][i] == player:
                count += 1
    if count == 3:
        return True
    else:
        count = 0
    if (x == 0 and y == 2) or (x == 2 and y == 0) or (x == 1 and y == 1):
        for i in range(3):
            if mat[i][2-i] == player:
                count += 1
    if count == 3:
        return True
    
    return 0

def draw_circle(screen, i, j):
    x = WIDTH // 6
    y = (HEIGHT - TEXT_SPACE) // 6
    pygame.draw.circle(screen, PLAYER1, (x*i*2 + x, y*j*2 + y + TEXT_SPACE), min(x, y) // 2, int(min(x//2, y//2) * 1/4))

def draw_cross(screen, i, j):
    x = WIDTH // 12
    y = (HEIGHT - TEXT_SPACE) // 12
    pygame.draw.line(screen, PLAYER2, (x*i*4 + x, y*j*4 + y + TEXT_SPACE), (x*i*4 + 3*x, y*j*4 + 3*y + TEXT_SPACE), int(min(x, y) * 1/4))
    pygame.draw.line(screen, PLAYER2, (x*i*4 + 3*x, y*j*4 + y + TEXT_SPACE), (x*i*4 + x, y*j*4 + 3*y + TEXT_SPACE), int(min(x, y) * 1/4))

def get_matrix_pos(x, y, mat):
    x = x // (WIDTH // 3)
    y = (y - TEXT_SPACE) // ((HEIGHT - TEXT_SPACE) // 3)
    return x, y

def add_token(x, y, mat, turn):
    if mat[x][y] == 0:
        mat[x][y] = (turn + 1)
        return True
    else:
        return False

def display_frame(screen):
    screen.fill(BACKGROUND)

    # Dibujando el tablero
    w = WIDTH // 3
    h = (HEIGHT - TEXT_SPACE) // 3
    for i in range(1, 3):
        vertical_divisor = i * w
        horizontal_divisor = i * h
        pygame.draw.line(screen, DETAILS_COLOR, (vertical_divisor, 0 + TEXT_SPACE), (vertical_divisor, HEIGHT + TEXT_SPACE), 7)
        pygame.draw.line(screen, DETAILS_COLOR, (0, horizontal_divisor + TEXT_SPACE), (WIDTH , horizontal_divisor + TEXT_SPACE), 7)
    
    for i in range(3):
        for j in range(3):
            if mat[i][j] == 1:
                draw_circle(screen, i, j)
            elif mat[i][j] == 2:
                draw_cross(screen, i, j)

    # Dibujar zona texto
    text_zone = pygame.Rect(0, 0, WIDTH, TEXT_SPACE)
    pygame.draw.rect(screen, DETAILS_COLOR, text_zone, width=0)

    text = "Player {} turn".format(turn + 1)
    draw_text(screen, text, TEXT_SPACE // 2, WIDTH // 2, TEXT_SPACE // 2)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicTacToe")
clock = pygame.time.Clock()

mat = [[0 for _ in range(3)] for _ in range(3)]

game_over = False
running = True
winner = 0
turn = 0
tokens = 0
last_movement_valid = True

while running:
    clock.tick(60)
    if game_over:
        game_over = game_over_message(winner)
        if game_over:
            break
        else:
            winner = 0
            turn = 0
            tokens = 0
            mat = [[0 for _ in range(3)] for _ in range(3)]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            x, y = get_matrix_pos(x, y, mat)
            last_movement_valid = add_token(x, y, mat, turn)
            if last_movement_valid:
                tokens += 1
                if check_win(x, y, turn+1, mat):
                    winner = turn + 1
                    game_over = True
                elif tokens == 9:
                    game_over = True
                else:
                    turn = (turn + 1) % 2                

    display_frame(screen)

    pygame.display.flip()
pygame.quit()