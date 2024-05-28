import pygame
from sys import exit
from random import randint


def display_score():
    current_time = pygame.time.get_ticks() // 1000 - start_time
    score_surface = text_font.render("SCORE: " + f'{current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(450, 50))
    screen.blit(score_surface, score_rect)


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 7
            if obstacle_rect.bottom == 500:
                snail_animation()
                screen.blit(snail_surface, obstacle_rect)
            else:
                fly_animation()
                screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle_rect for obstacle_rect in obstacle_list if obstacle_rect.x > -100]
        return obstacle_list
    else:
        return []


def collision(player, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_index, player_surface
    if player_rect.bottom < 500:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index > len(player_list):
            player_index = 0
        player_surface = player_list[int(player_index)]


def snail_animation():
    global snail_index, snail_surface
    snail_index += 0.1
    if snail_index > len(snail_list):
        snail_index = 0
    snail_surface = snail_list[int(snail_index)]


def fly_animation():
    global fly_index, fly_surface
    fly_index += 0.1
    if fly_index > len(fly_list):
        fly_index = 0
    fly_surface = fly_list[int(fly_index)]


start_time = 0

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption('runner')

# Set up the clock
clock = pygame.time.Clock()

# Snowfall parameters
snowflakes = []

# Load fonts and images
text_font = pygame.font.Font(None, 50)
background_surface = pygame.image.load('graphics/sky2.jpg').convert_alpha()
ground_surface = pygame.image.load('graphics/ground2.png').convert_alpha()

player_jump = pygame.image.load('graphics/santa_jump.png').convert_alpha()
player1 = pygame.image.load('graphics/santa1.png').convert_alpha()
player2 = pygame.image.load('graphics/santa2.png').convert_alpha()
player_list = [player1, player2]
player_index = 0
player_surface = player_list[player_index]

snail1 = pygame.image.load('graphics/snail1.png').convert_alpha()
snail2 = pygame.image.load('graphics/snail2.png').convert_alpha()
snail_list = [snail1, snail2]
snail_index = 0
snail_surface = snail_list[snail_index]

fly1 = pygame.image.load('graphics/fly1.png').convert_alpha()
fly2 = pygame.image.load('graphics/fly2.png').convert_alpha()
fly_list = [fly1, fly2]
fly_index = 0
fly_surface = fly_list[fly_index]

# Set up rectangles for images
background_rect = background_surface.get_rect(topleft=(0, 0))
ground_rect = ground_surface.get_rect(topleft=(0, 500))
player_rect = player_surface.get_rect(midbottom=(120, 500))

# obstacle list
obstacle_rect_list = []

# Initialize player gravity and game state
player_gravity = 0
game_active = True

# Load background music
pygame.mixer.music.load('graphics/jingle-bells-58.mp3')
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely

# Load jump sound
jump_sound = pygame.mixer.Sound('graphics/sleigh-bell-long-01-38409.mp3')

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

# Main game loop
while True:
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 500 and game_active:
            player_gravity = -20
            jump_sound.play()  # Play jump sound
        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 500)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 320)))

    if game_active:
        # background and ground
        screen.blit(background_surface, background_rect)
        screen.blit(ground_surface, ground_rect)

        # display score
        display_score()

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision(player_rect, obstacle_rect_list)

        # jumping to using space key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and player_rect.bottom >= 500:
            player_gravity = -20
            jump_sound.play()  # Play jump sound

        # player gravity
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 500:
            player_rect.bottom = 500
        player_animation()
        screen.blit(player_surface, player_rect)

        # Create and update snowfall
        snowflakes.append([randint(0, 900), 0, randint(1, 5)])
        for flake in snowflakes:
            pygame.draw.circle(screen, (255, 255, 255), flake[:2], flake[2])
            flake[1] += 2
            if flake[1] > 500:
                flake[1] = 700
                flake[0] = randint(0, 900)

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_active = True
            obstacle_rect_list = []
        start_time = pygame.time.get_ticks() // 1000
        score_surface2 = text_font.render("MERRY CHRISTMAS", False, (255, 0, 0))
        score_rect2 = score_surface2.get_rect(center=(450, 300))
        screen.blit(score_surface2, score_rect2)
