import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Katana Fighting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player variables
player_width = 50
player_height = 100
player_x = window_width // 4 - player_width // 2
player_y = window_height - player_height
player_speed = 5
player_attack_cooldown = 30
player_attack_duration = 10
player_attacking = False

# Enemy variables
enemy_width = 50
enemy_height = 100
enemy_x = 3 * window_width // 4 - enemy_width // 2
enemy_y = window_height - enemy_height
enemy_speed = 5
enemy_attack_cooldown = 30
enemy_attack_duration = 10
enemy_attacking = False

clock = pygame.time.Clock()
game_over = False

def draw_player():
    pygame.draw.rect(window, WHITE, (player_x, player_y, player_width, player_height))

def draw_enemy():
    pygame.draw.rect(window, RED, (enemy_x, enemy_y, enemy_width, enemy_height))

def check_collision():
    if player_attacking:
        if player_y + player_height >= enemy_y and player_y <= enemy_y + enemy_height:
            if player_x + player_width >= enemy_x and player_x <= enemy_x + enemy_width:
                return True
    elif enemy_attacking:
        if enemy_y + enemy_height >= player_y and enemy_y <= player_y + player_height:
            if enemy_x + enemy_width >= player_x and enemy_x <= player_x + player_width:
                return True
    return False

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    # Player movement
    if keys[pygame.K_a] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_d] and player_x < window_width - player_width:
        player_x += player_speed

    # Player attack
    if keys[pygame.K_SPACE] and player_attack_cooldown <= 0:
        player_attacking = True
        player_attack_cooldown = 30
    elif player_attacking and player_attack_duration <= 0:
        player_attacking = False
        player_attack_duration = 10

    # Enemy movement
    if keys[pygame.K_LEFT] and enemy_x > 0:
        enemy_x -= enemy_speed
    if keys[pygame.K_RIGHT] and enemy_x < window_width - enemy_width:
        enemy_x += enemy_speed

        # Enemy attack
        if enemy_attack_cooldown <= 0:
            enemy_attacking = True
            enemy_attack_cooldown = 60
        elif enemy_attacking and enemy_attack_duration <= 0:
            enemy_attacking = False
            enemy_attack_duration = 15

    # Collision check
    if check_collision():
        game_over = True

    # Clear the screen
    window.fill(BLACK)

    # Draw the player and enemy
    draw_player()
    draw_enemy()

    # Update the display
    pygame.display.update()
    clock.tick(60)

    # Decrement attack cooldowns and durations
    player_attack_cooldown -= 1
    player_attack_duration -= 1
    enemy_attack_cooldown