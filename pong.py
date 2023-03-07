import pygame
pygame.init()

PLAYER_SPEED = 5
BALL_SPEED = 5

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
screen_size = (800, 600)
player_width = 15
player_height = 90

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# Coordenadas y velocidad del jugador 1
player1_x_coor = 50
player1_y_coor = 300 - 45
player1_y_speed = 0

# Coordenadas y velocidad del jugador 2
player2_x_coor = 750 - player_width
player2_y_coor = 300 - 45
player2_y_speed = 0

# Coordenadas de la pelota
pelota_x = 400
pelota_y = 300
pelota_speed_x = BALL_SPEED
pelota_speed_y = BALL_SPEED

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            # Jugador 1
            if event.key == pygame.K_w:
                player1_y_speed -= PLAYER_SPEED
            if event.key == pygame.K_s:
                player1_y_speed += PLAYER_SPEED
            # Jugador 2
            if event.key == pygame.K_UP:
                player2_y_speed -= PLAYER_SPEED
            if event.key == pygame.K_DOWN:
                player2_y_speed += PLAYER_SPEED
        
        if event.type == pygame.KEYUP:
            # Jugador 1
            if event.key == pygame.K_w:
                player1_y_speed += PLAYER_SPEED
            if event.key == pygame.K_s:
                player1_y_speed -= PLAYER_SPEED
            # Jugador 2
            if event.key == pygame.K_UP:
                player2_y_speed += PLAYER_SPEED
            if event.key == pygame.K_DOWN:
                player2_y_speed -= PLAYER_SPEED

    if pelota_y > 590 or pelota_y < 10:
        pelota_speed_y *= -1
    
    # Revisa si la pelota sale del lado derecho
    if pelota_x > 800 or pelota_x < 0:
        pelota_x = 400
        pelota_y = 300
        # Si sale de la patalla, invierte direccion
        pelota_speed_x *= -1
        pelota_speed_y *= 0

    # Modifica las coordenadas para dar mov. a los jugadores/pelota
    player1_y_coor += player1_y_speed
    player2_y_coor += player2_y_speed

    if player1_y_coor > 510:
        player1_y_coor = 510
    if player1_y_coor < 0:
        player1_y_coor = 0

    if player2_y_coor > 510:
        player2_y_coor = 510
    if player2_y_coor < 0:
        player2_y_coor = 0

    # Movimiento pelota
    pelota_x += pelota_speed_x
    pelota_y += pelota_speed_y

    screen.fill(black)

    # Zona de dibujo
    for i in range(12, 600, 50):
        pygame.draw.rect(screen, white, (390, i, 20, 25))

    jugador1 = pygame.draw.rect(screen, white, (player1_x_coor, player1_y_coor, player_width, player_height))
    jugador2 = pygame.draw.rect(screen, white, (player2_x_coor, player2_y_coor, player_width, player_height))
    pelota = pygame.draw.circle(screen, white, (pelota_x, pelota_y), 10)

    # Colisiones
    if pelota.colliderect(jugador1):
        pelota_speed_y = -(player1_y_coor + 45 - pelota_y)/3
        pelota_speed_x *= -1
    elif pelota.colliderect(jugador2):
        pelota_speed_y = -(player2_y_coor + 45 - pelota_y)/3
        pelota_speed_x *= -1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()