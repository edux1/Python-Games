import pygame, random

# COLORES
BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BACKGROUND = (51, 181, 255)

CELL_SIZE = 23

COLUMNS = ROWS = 9
BOMBS = 10

size = (COLUMNS * CELL_SIZE, ROWS * CELL_SIZE)

def display_frame(x, y):
    screen.fill(BACKGROUND)
    for i in range(COLUMNS):
        for j in range(ROWS):
            image = pygame.image.load(png_list[mat[i][j]]).convert()
            image = pygame.transform.scale(image, (23, 23))
            screen.blit(image,[i*CELL_SIZE, j*CELL_SIZE])
    if x != -1 and y != -1 and mat[x][y] == 9:
        image = pygame.image.load(png_list[0]).convert()
        image = pygame.transform.scale(image, (23, 23))
        screen.blit(image,[x*CELL_SIZE, y*CELL_SIZE])

    pygame.display.flip()

def get_mat_pos(x, y):
    x //= CELL_SIZE
    y //= CELL_SIZE
    return x, y

def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    return get_mat_pos(x, y)

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
    print(mine_list)


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
    print(visited)
    if mat[x][y] == 9:
        if solution[x][y] == 0:
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if i >= 0 and i < COLUMNS and j >= 0 and j < ROWS and not (i,j) in visited:
                        print("RECURSION")
                        visited.append((i,j))
                        show_cell(i, j, visited)
        mat[x][y] = solution[x][y]

def print_mat(mat):
    for i in range(ROWS):
        print(mat[i])

pygame.init()

png_list = ["assets/0.png", "assets/1.png", "assets/2.png", "assets/3.png", "assets/4.png", 
            "assets/5.png", "assets/6.png", "assets/7.png", "assets/8.png", "assets/9_unclicked.png",
            "assets/10_flag.png", "assets/11_mine.png", "assets/12_mine_boom.png"]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

mat = [[9 for _ in range(ROWS)] for _ in range(ROWS)]
solution = [[0 for _ in range(ROWS)] for _ in range(ROWS)]
mine_list = []
print_mat(mat)


running = True
first_click = True

pos_x, pos_y = -1, -1

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:
            pos_x, pos_y = get_mouse_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = get_mouse_pos()
            if first_click:
                generate_escenary(x, y)
                first_click = False
            show_cell(x, y, [(x,y)])
            pos_x, pos_y = -1, -1


    display_frame(pos_x, pos_y)

pygame.quit()