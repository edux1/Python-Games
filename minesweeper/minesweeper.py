import pygame, random, time

# COLORES
BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BACKGROUND = (185,185,185)

FACE_SIZE = 32
CELL_SIZE = 23

TOP_BAR_SIZE = 50
BOTTOM_BAR_SIZE = 50

COLUMNS = ROWS = 9
BOMBS = 10

size = (COLUMNS * CELL_SIZE, ROWS * CELL_SIZE + TOP_BAR_SIZE + BOTTOM_BAR_SIZE)

def display_frame(x, y):
    screen.fill(BACKGROUND)
    for i in range(COLUMNS):
        for j in range(ROWS):
            image = pygame.image.load(png_list[mat[i][j]]).convert()
            image = pygame.transform.scale(image, (23, 23))
            screen.blit(image,[i*CELL_SIZE, j*CELL_SIZE + TOP_BAR_SIZE])
    draw_face(x, y)
    draw_timer()
    draw_bomb_countdown()
    draw_buttons()
    pygame.display.flip()

def draw_button(text, x, y, color):
    draw_text(screen, text, 14, x, y, color)
    pygame.draw.line(screen, BLACK, (x+30,y-BOTTOM_BAR_SIZE//4+20), (x+30, y-BOTTOM_BAR_SIZE//4), width=1)
    pygame.draw.line(screen, BLACK, (x-30,y-BOTTOM_BAR_SIZE//4+20), (x+30, y-BOTTOM_BAR_SIZE//4+20), width=1)
    pygame.draw.line(screen, WHITE, (x-30, y-BOTTOM_BAR_SIZE//4), (x+30,y-BOTTOM_BAR_SIZE//4), width=1)
    pygame.draw.line(screen, WHITE, (x-30, y-BOTTOM_BAR_SIZE//4), (x-30,y-BOTTOM_BAR_SIZE//4+20), width=1)

def draw_buttons():
    draw_button("EASY", 35, TOP_BAR_SIZE + CELL_SIZE*ROWS + BOTTOM_BAR_SIZE//2, BLUE)
    draw_button("MEDIUM", COLUMNS*CELL_SIZE//2, TOP_BAR_SIZE + CELL_SIZE*ROWS + BOTTOM_BAR_SIZE//2, YELLOW)
    draw_button("HARD", COLUMNS*CELL_SIZE - 35, TOP_BAR_SIZE + CELL_SIZE*ROWS + BOTTOM_BAR_SIZE//2, RED)

def draw_text(surface, text, size, x, y, color):
    font = pygame.font.SysFont("calibri", size, bold=True)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def draw_timer():
    hundredths = elapsed_time // 100
    tenths = (elapsed_time - (hundredths * 100)) // 10 
    units = elapsed_time % 10
    x = COLUMNS*CELL_SIZE - 10
    y = TOP_BAR_SIZE//2-20
    draw_number(units, x-23, y)
    draw_number(tenths, x-(23*2), y)
    draw_number(hundredths, x-(23*3), y)

def draw_bomb_countdown():
    countdown = BOMBS - len(flag_list)
    negative_hundreths = False
    negative_tenths = False
    if countdown < -9:
        negative_hundreths = True
    elif countdown < 0:
        negative_tenths = True
    countdown = abs(countdown)
    hundredths = countdown // 100
    tenths = (countdown - (hundredths * 100)) // 10 
    units = countdown - (hundredths*100 + tenths*10)
    x = 10
    y = TOP_BAR_SIZE//2-20    
    draw_number(units, x+23*2, y)
    draw_number(tenths, x+23, y, negative_tenths)
    draw_number(hundredths, x, y, negative_hundreths)

def draw_number(num, x, y, negative=False):
    if negative:
        number = pygame.image.load("assets/negative.png").convert()
    else:
        number = pygame.image.load(numbers_list[num]).convert()
    screen.blit(number, [x, y])

def draw_face(x, y):
    if not game_over:
        if x >= 0 and ROWS > y >= 0 and mat[x][y] == 9:
            image = pygame.image.load(png_list[0]).convert()
            image = pygame.transform.scale(image, (23, 23))
            screen.blit(image,[x*CELL_SIZE, y*CELL_SIZE + TOP_BAR_SIZE])
        face_image = pygame.image.load("assets/smile_face.png").convert()
    elif win:
        face_image = pygame.image.load("assets/winner_face.png").convert()
    else:
        face_image = pygame.image.load("assets/death_face.png").convert()
    face_image = pygame.transform.scale(face_image, (FACE_SIZE, FACE_SIZE))
    face_image_rect = face_image.get_rect()
    face_image_rect.center = (CELL_SIZE*COLUMNS/2, TOP_BAR_SIZE//2)
    screen.blit(face_image, face_image_rect)

def check_buttons(x, y):
    easy_bt = pygame.Rect((5, TOP_BAR_SIZE + CELL_SIZE*ROWS + BOTTOM_BAR_SIZE//4), (61, 22))
    medium_bt = pygame.Rect((COLUMNS*CELL_SIZE//2-30, TOP_BAR_SIZE + CELL_SIZE*ROWS + BOTTOM_BAR_SIZE//4), (61, 22))
    hard_bt = pygame.Rect((COLUMNS*CELL_SIZE-65, TOP_BAR_SIZE + CELL_SIZE*ROWS + BOTTOM_BAR_SIZE//4), (61, 22))
    if easy_bt.collidepoint(x, y):
        return 1
    if medium_bt.collidepoint(x, y):
        return 2
    if hard_bt.collidepoint(x, y):
        return 3
    return 0

def get_mat_pos(x, y):
    y -= TOP_BAR_SIZE 
    x //= CELL_SIZE
    y //= CELL_SIZE
    return x, y

def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    return x, y

def generate_bombs(x, y):
    col, row = x, y
    for i in range(BOMBS):
        col = random.randrange(0, COLUMNS)
        row = random.randrange(0, ROWS)
        while col == x and row == y or solution[col][row] == 11:
            col = random.randrange(0, COLUMNS)
            row = random.randrange(0, ROWS)
        mine_list.append((col, row))
        solution[col][row] = 11

def calculate_other_cells():
    for mine in mine_list:
        x,y  = mine[0], mine[1]
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and i < COLUMNS and j >= 0 and j < ROWS and solution[i][j] != 11:
                    solution[i][j] += 1

def generate_escenary(x, y):
    generate_bombs(x, y)
    calculate_other_cells();
    
def show_cell(x, y, visited):
    game_over = False
    global countdown
    if mat[x][y] == 9:
        if solution[x][y] == 0:
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if i >= 0 and i < COLUMNS and j >= 0 and j < ROWS and not (i,j) in visited:
                        visited.append((i,j))
                        game_over = show_cell(i, j, visited)
        if solution[x][y] == 11:
            mat[x][y] = 12
            game_over = True
        else:
            mat[x][y] = solution[x][y]
            countdown -= 1
    return game_over

def show__neighbour_cells(x, y):
    game_over = False
    count = mat[x][y]
    global countdown
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i >= 0 and i < COLUMNS and j >= 0 and j < ROWS and mat[i][j] == 10:
                count -= 1
    if count == 0:
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and i < COLUMNS and j >= 0 and j < ROWS and mat[i][j] == 9:
                    if solution[i][j] == 0:
                        game_over = show_cell(i, j, [(i, j)]) or game_over
                    else:
                        if solution[i][j] == 11:
                            mat[i][j] = 12
                            game_over = True
                        else:
                            mat[i][j] = solution[i][j]
                            countdown -= 1
    return game_over

def show_all_bombs():
    for mine in mine_list:
        x, y = mine[0], mine[1]
        if mat[x][y] == 9:
            mat[x][y] = 11

def show_wrong_flags():
    for flag in flag_list:
        x, y = flag[0], flag[1]
        if mat[x][y] != 10:
            mat[x][y] = 13

def convert_unclicked_to_flag():
    for mine in mine_list:
        x, y = mine[0], mine[1]
        if mat[x][y] != 10:
            flag_list.append((x, y))
        mat[x][y] = 10

def switch_flag(x, y):
    if mat[x][y] == 9:
        mat[x][y] = 10
        flag_list.append((x, y))
    elif mat[x][y] == 10:
        mat[x][y] = 9
        flag_list.remove((x,y))

pygame.init()

png_list = ["assets/0.png", "assets/1.png", "assets/2.png", "assets/3.png", "assets/4.png", 
            "assets/5.png", "assets/6.png", "assets/7.png", "assets/8.png", "assets/9_unclicked.png",
            "assets/10_flag.png", "assets/11_mine.png", "assets/12_mine_boom.png", "assets/13_red_flag.png"]

numbers_list = ["assets/number_0.png", "assets/number_1.png", "assets/number_2.png", "assets/number_3.png",
                "assets/number_4.png", "assets/number_5.png", "assets/number_6.png", "assets/number_7.png",
                "assets/number_8.png", "assets/number_9.png"]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

mat = [[9 for _ in range(ROWS)] for _ in range(ROWS)]
solution = [[0 for _ in range(ROWS)] for _ in range(ROWS)]
mine_list = []
flag_list = []

running = True
first_click = True
game_over = False
win = False
countdown = COLUMNS * ROWS - BOMBS
start_time = None
elapsed_time = 0

face_image_rect = pygame.Rect((0,0), (FACE_SIZE, FACE_SIZE))
face_image_rect.center = (CELL_SIZE*ROWS//2, TOP_BAR_SIZE//2)

pos_x, pos_y = -1, -1

while running:
    clock.tick(15)
    if start_time and not game_over:
        elapsed_time = int(time.time() - start_time)
    if game_over:
        if win:
            convert_unclicked_to_flag()
        else:
            show_all_bombs()
            show_wrong_flags()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:
            pos_x, pos_y = get_mouse_pos()
            pos_x, pos_y = get_mat_pos(pos_x, pos_y)
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = get_mouse_pos()
            if face_image_rect.collidepoint(x, y):
                # Restarting game
                elapsed_time = 0
                start_time = None
                mine_list = []
                flag_list = []
                game_over = False
                first_click = True
                win = False
                countdown = COLUMNS * ROWS - BOMBS
                mat = [[9 for _ in range(ROWS)] for _ in range(COLUMNS)]
                solution = [[0 for _ in range(ROWS)] for _ in range(COLUMNS)]
            elif COLUMNS*CELL_SIZE > x >= 0 and ROWS*CELL_SIZE+TOP_BAR_SIZE+BOTTOM_BAR_SIZE> y > ROWS*CELL_SIZE+TOP_BAR_SIZE:
                button_clicked = check_buttons(x,y)
                if button_clicked == 1:
                    COLUMNS = ROWS = 9
                    BOMBS = 10
                    screen = pygame.display.set_mode((COLUMNS * CELL_SIZE, ROWS * CELL_SIZE + TOP_BAR_SIZE + BOTTOM_BAR_SIZE))
                elif button_clicked == 2:
                    COLUMNS = ROWS = 16
                    BOMBS = 40
                    screen = pygame.display.set_mode((COLUMNS * CELL_SIZE, ROWS * CELL_SIZE + TOP_BAR_SIZE + BOTTOM_BAR_SIZE))
                elif button_clicked == 3:
                    COLUMNS = 30
                    ROWS = 16
                    BOMBS = 99
                    screen = pygame.display.set_mode((COLUMNS * CELL_SIZE, ROWS * CELL_SIZE + TOP_BAR_SIZE + BOTTOM_BAR_SIZE))
                if button_clicked != 0:
                    # Restarting game
                    elapsed_time = 0
                    start_time = None
                    mine_list = []
                    flag_list = []
                    game_over = False
                    first_click = True
                    win = False
                    countdown = COLUMNS * ROWS - BOMBS
                    mat = [[9 for _ in range(ROWS)] for _ in range(COLUMNS)]
                    solution = [[0 for _ in range(ROWS)] for _ in range(COLUMNS)]
                    face_image_rect = pygame.Rect((0,0), (FACE_SIZE, FACE_SIZE))
                    face_image_rect.center = (CELL_SIZE*COLUMNS//2, TOP_BAR_SIZE//2)
                    pos_x, pos_y = -1, -1
            else:
                x, y = get_mat_pos(x, y)
                # event.button 1 - Left click
                # event.button 3 - Right click
                if not game_over:               
                    if x >= 0 and ROWS > y >= 0:
                        if event.button == 1:   
                            if first_click:
                                generate_escenary(x, y)
                                first_click = False
                                start_time = time.time()
                            if mat[x][y] == 9:
                                game_over = show_cell(x, y, [(x,y)])
                            elif 0 < mat[x][y] < 9:
                                game_over = show__neighbour_cells(x, y)
                            pos_x, pos_y = -1, -1
                        elif event.button == 3:
                            switch_flag(x, y)
                        if countdown == 0:
                            game_over = True
                            win = True
    display_frame(pos_x, pos_y)

pygame.quit()