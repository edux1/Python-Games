import pygame

TEXT_SPACE = 150
CELL_SIZE = 100
WIDTH = 7 * CELL_SIZE
HEIGHT = 6 * CELL_SIZE + TEXT_SPACE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED_LIGHT = (235, 114, 106)
YELLOW = (237, 237, 85)
BACKGROUND = (50, 98, 168)

def display_frame():
    screen.fill(BACKGROUND)
    print_table()
    hover_cell()
    if winner == 0 and not game_over:
        if turn == 0:
            draw_text(screen, "RED's turn", TEXT_SPACE//2, WIDTH//2, TEXT_SPACE//2, RED_LIGHT)
        else:
            draw_text(screen, "YELLOW's turn", TEXT_SPACE//2, WIDTH//2, TEXT_SPACE//2, YELLOW)

    pygame.display.flip()

def draw_text(surface, text, size, x, y, color):
    font = pygame.font.SysFont("calibri", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def get_column():
    column, _ = pygame.mouse.get_pos()
    column //= CELL_SIZE
    return column

def find_first_cell_free(column):
    if column < 7:
        for i in range(5,-1,-1):
            if mat[i][column] == 0:
                return i
    return -1

def hover_cell():
    if not game_over:
        column = get_column()
        row = find_first_cell_free(column)
        if row >= 0:
            pygame.draw.circle(screen, BLACK, (CELL_SIZE // 2 + CELL_SIZE*column, CELL_SIZE // 2 + CELL_SIZE*row  + TEXT_SPACE), CELL_SIZE // 3, width=3)

def check_vertical(row, column, player):
    count = 0
    for i in range(1, 6 - row):
        if mat[row+i][column] == player:
            count += 1
            if count == 3:
                print("VERTICAL")
                return player
        else:
            break
    return 0
        
def check_horizontal(row, column, player):
    count = 0
    # to the right
    for i in range(1, 7 - column):
        if mat[row][column+i] == player:
            count += 1
            if count == 3:
                print("HORIZONTAL1")
                return player
        else:
            break
    # to the left
    for i in range(1, column+1):
        if mat[row][column-i] == player:
            count += 1
            if count == 3:
                print("HORIZONTAL2")
                return player
        else:
            break
    return 0

def check_diagonal_1(row, column, player):
    count = 0
    # to the bottom-right
    for i in range(1, min(6-row, 7-column)):
        if mat[row+i][column+i] == player:
            count += 1
            if count == 3:
                print("DIAGONAL1.1")
                return player
        else:
            break
    # to the top-left
    print(count)
    for i in range(1, min(row+1, column+1)):
        print(row-i, column-i, i)
        if mat[row-i][column-i] == player:
            count += 1
            if count == 3:
                print("DIAGONAL1.2")
                return player
        else:
            break
    return 0

def check_diagonal_2(row, column, player):
    count = 0
    # to the top-right
    for i in range(1, min(row+1, 7-column)):
        if mat[row-i][column+i] == player:
            count += 1
            if count == 3:
                print("DIAGONAL2.1")
                return player
        else:
            break
    # to te bottom-left
    for i in range(1, min(6-row, column+1)):
        if mat[row+i][column-i] == player:
            count += 1
            if count == 3:
                print("DIAGONAL2.2")
                return player
        else:
            break
    return 0

def check_win(row, column, player):
    if check_vertical(row, column, player) or check_horizontal(row, column, player) \
        or check_diagonal_1(row, column, player) or check_diagonal_2(row, column, player):   
        return player
    return 0

def print_table():
    for i in range(6):
        for j in range(7):
            if mat[i][j] == 0:
                pygame.draw.circle(screen, WHITE, (CELL_SIZE // 2 + CELL_SIZE*j, CELL_SIZE // 2 + CELL_SIZE*i + TEXT_SPACE), CELL_SIZE // 3, width=0)
            elif mat[i][j] == 1:
                pygame.draw.circle(screen, RED, (CELL_SIZE // 2 + CELL_SIZE*j, CELL_SIZE // 2 + CELL_SIZE*i + TEXT_SPACE), CELL_SIZE // 3, width=0)
            else:
                pygame.draw.circle(screen, YELLOW, (CELL_SIZE // 2 + CELL_SIZE*j, CELL_SIZE // 2 + CELL_SIZE*i + TEXT_SPACE), CELL_SIZE // 3, width=0)
    pass

def game_over_message(winner):
    if winner == 0:
        draw_text(screen, "IT'S A DRAW", TEXT_SPACE // 2, WIDTH // 2, TEXT_SPACE // 2, WHITE)
    elif winner == 1:
        draw_text(screen, "RED WON", TEXT_SPACE // 2, WIDTH // 2, TEXT_SPACE // 2, RED_LIGHT)
    else:
        draw_text(screen, "YELLOW WON", TEXT_SPACE // 2, WIDTH // 2, TEXT_SPACE // 2, YELLOW)
    
    draw_text(screen, "Press SPACE to play again", TEXT_SPACE // 5, WIDTH // 2, TEXT_SPACE * 4/5, WHITE)
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

# ===== GAME =====

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")
clock = pygame.time.Clock()

mat = [[0 for _ in range(7)] for _ in range(6)]

game_over = False
running = True
winner = 0
turn = 0
moves = 0

while running:
    clock.tick(60)
    if game_over:
        game_over = game_over_message(winner)
        if game_over:
            break
        else:
            winner = 0
            turn = 0
            moves = 0
            mat = mat = [[0 for _ in range(7)] for _ in range(6)]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:
            column = get_column()
            row = find_first_cell_free(column)
            if row != -1:
                if turn == 0:
                    mat[row][column] = 1
                else:
                    mat[row][column] = 2
                moves += 1
                winner = check_win(row, column, turn + 1)
                print(moves)
                if winner != 0 or moves == 6*7:
                    game_over = True
                turn = (turn + 1) % 2
    display_frame()

pygame.quit()